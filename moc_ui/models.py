from django.db import models
from passlib.hash import sha512_crypt
import json

from keystoneclient.v2_0 import client as keystoneclient
from keystoneclient.exceptions import AuthorizationFailure

# Lengths for CharField, as it is required
PASSHASH_LEN = len(sha512_crypt.encrypt(''))
DEFAULT_FIELD_LEN = 255


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


class Cluster(models.Model):
     """An openstack cluster."""
     title = models.CharField(max_length=DEFAULT_FIELD_LEN)
     auth_url = models.URLField()

     def __unicode__(self):
         return self.title


class ClusterAccount(models.Model):
     """A user account within an openstack cluster.

     Each of these belongs to a marketplace UI user. We store that user's
     openstack credentials in the database, including username/password,
     and posibly a keystone token, if we have a valid one.

     Users of this class should verify that the token is still valid before
     trying to use it, and fetch a new one if needed.
     """
     user = models.ForeignKey(User)
     cluster = models.ForeignKey(Cluster)
     cluster_username = models.CharField(max_length=DEFAULT_FIELD_LEN)
     cluster_password = models.CharField(max_length=DEFAULT_FIELD_LEN)
     token = models.TextField(default=None, blank=True, null=True)

     def __unicode__(self):
         return '%r@%r' % (self.cluster_username, self.cluster.title)


     def get_keystoneclient(self):
         """Get a keystone client object for the cluster account.

        Returns the client object.

        This may raise ``keystone.exceptions.AuthorizationFailure`` if
        authorization fails for any reason, including stale tokens in
        the database. At some point we'll want to have that handle within
        this method, but for now, just try again -- the stale token will
        have been deleted.
         """
         try:
            if self.token is None:
                client = keystoneclient.Client(username=self.cluster_username,
                                                password=self.cluster_password,
                                                auth_url=self.cluster.auth_url,
                                                )
                self.token = json.dumps(client.auth_ref)
            else:
                client = keystoneclient.Client(auth_ref=json.loads(self.token))
            client.authenticate()
         except AuthorizationFailure:
            self.token = None
            raise
