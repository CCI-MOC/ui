from django.db import models
from passlib.hash import sha512_crypt
import json
import uuid

from keystoneclient.v2_0 import client as keystoneclient
from keystoneclient.exceptions import AuthorizationFailure
from novaclient.v2 import client as novaclient

# Lengths for CharField, as it is required
PASSHASH_LEN = len(sha512_crypt.encrypt(''))
UUID_LEN = len(str(uuid.uuid1()))
DEFAULT_FIELD_LEN = 255


# user specifics
class User(models.Model):
    """A user of the marketplace UI"""
    name = models.CharField(primary_key=True, max_length=DEFAULT_FIELD_LEN)
    password_hash = models.CharField(max_length=PASSHASH_LEN)

    def verify_password(self, password):
        return sha512_crypt.verify(password, self.password_hash)

    def set_password(self, password):
        self.password_hash = sha512_crypt.encrypt(password)

    def __unicode__(self):
        return self.name


class UIProject(models.Model):
    """A user's project in the moc ui."""
    user = models.ForeignKey(User)

    name = models.CharField(max_length=DEFAULT_FIELD_LEN)

    def __unicode__(self):
        return self.name


class Cluster(models.Model):
    """An openstack cluster."""
    title = models.CharField(max_length=DEFAULT_FIELD_LEN)
    auth_url = models.URLField()

    def __unicode__(self):
        return self.title


class ClusterAccount(models.Model):
    """A user account within an openstack cluster.

    Each of these belongs to a marketplace UI user. We store that user's
    openstack credentials in the database, including username/password.
    These are used by OSProject to obtain a token when necessary.
    """
    user = models.ForeignKey(User)
    cluster = models.ForeignKey(Cluster)
    cluster_username = models.CharField(max_length=DEFAULT_FIELD_LEN)
    cluster_password = models.CharField(max_length=DEFAULT_FIELD_LEN)

    def __unicode__(self):
        return '%r@%r' % (self.cluster_username, self.cluster.title)


class OSProject(models.Model):
    """An openstack project that a user has access to."""
    name = models.CharField(max_length=DEFAULT_FIELD_LEN)
    cluster_account = models.ForeignKey(ClusterAccount)
    token = models.TextField(default=None, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_keystoneclient(self):
        """Get a keystone client object for the tenant.

        Returns the client object.

        This may raise ``keystone.exceptions.AuthorizationFailure`` if
        authorization fails for any reason, including stale tokens in
        the database.
        """
        try:
            if self.token is None:
                client = keystoneclient.Client(username=self.cluster_account.cluster_username,
                                               password=self.cluster_account.cluster_password,
                                               auth_url=self.cluster_account.cluster.auth_url,
                                               tenant_name=self.name,
                                               )
                self.token = json.dumps(client.auth_ref)
            else:
                client = keystoneclient.Client(auth_ref=json.loads(self.token))
            # keystoneclient authenticates lazily, i.e. It doensn't actually
            # authenticates until the first time it needs the token for
            # someting. We'd like to find out about failures now (in
            # particular, it's easier to clear a bad token here than somewhere
            # else in the code. authenticate() forces it to auth right now:
            client.authenticate()
            return client
        except AuthorizationFailure:
            # Clear the token if auth failed:
            self.token = None
            raise

    def get_novaclient(self):
        """Get a nova client for the tenant."""
        # TODO: We ought to be able to derive this from the keystone client,
        # but it's proving trickier than I expected --isd
        return novaclient.Client(self.cluster_account.cluster_username,
                                 self.cluster_account.cluster_password,
                                 self.name,
                                 self.cluster_account.cluster.auth_url)


class VM(models.Model):
    """A user's vm."""
    ui_project = models.ForeignKey(UIProject)
    os_project = models.ForeignKey(OSProject)
    os_uuid = models.CharField(max_length=UUID_LEN)

    def __unicode__(self):
        return self.name
