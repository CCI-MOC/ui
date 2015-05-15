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

# User information 
# Storing Password as PlainText for now! MASSIVELY STUPID IDEA
class User(models.Model):
    """A user of the marketplace UI"""
    user_name = models.CharField(primary_key=True, max_length=DEFAULT_FIELD_LEN)
    #password_hash = models.CharField(max_length=PASSHASH_LEN)
    password_hash = models.CharField(max_length=PASSHASH_LEN)
    
    def verify_password(self, password):
        return sha512_crypt.verify(password, self.password_hash)

    def set_password(self, password):
        self.password_hash = sha512_crypt.encrypt(password)

    def __unicode__(self):
        return self.user_name

    @classmethod
    def create_user(cls, user_name, password):
        new_user = cls(user_name=user_name)
        new_user.set_password(password)
        return new_user 

# A service in the marketplace
class Service(models.Model):
    """A service in the marketplace"""
    ## specifications for a service
    name = models.CharField(max_length=DEFAULT_FIELD_LEN)
    service_type = models.CharField(max_length=DEFAULT_FIELD_LEN)
    description = models.CharField(max_length=DEFAULT_FIELD_LEN)
    logo_url = models.CharField(max_length=DEFAULT_FIELD_LEN)
    availability = models.BooleanField(default=False)
    image_name = models.CharField(max_length = DEFAULT_FIELD_LEN)

    def __unicode__(self):
        return self.name

# Flavor for VM
# class Flavor (models.Model):
#     flavor =  models.CharField(max_length=DEFAULT_FIELD_LEN)
#     def __unicode__ (self):
#         return self.name


# Cluster information
class Cluster(models.Model):
    """An openstack installation available to users."""
    # CLUSTER_CHOICES = (('HARVARD_PROD', 'Harvard'),
    #                    ('NORTHEASTERN_PROD', 'Northeastern'),
    #                   )
    name = models.CharField(max_length=DEFAULT_FIELD_LEN,)
                               # choices=CLUSTER_CHOICES, 
                               # default='HARVARD_PROD')
    auth_url = models.URLField()

    def __unicode__(self):
        return self.name

# A project in our UI
class UIProject(models.Model):
    """A user's project in the moc ui."""
    ## Project information
    name = models.CharField(max_length=DEFAULT_FIELD_LEN)
    ## Foreign Keys
    users = models.ManyToManyField(User)

    ## Service Defaults 

    ## Registered Service Options
    service_list = models.ManyToManyField(Service, through = 'UIProject_service_list')

    def __unicode__(self):
        return self.name

# Joint_table for Service and Project
class UIProject_service_list(models.Model):
    TYPE_CHOICES = (('NOR','normal'), ('DEA', 'default'))
    project = models.ForeignKey(UIProject)
    service = models.ForeignKey(Service)
    type = models.CharField(max_length=DEFAULT_FIELD_LEN, choices=TYPE_CHOICES,  default='normal')

    def __unicode__(self):
        return 'Project Name: ' + self.project.name + ' Servise Name: ' + self.service.name + ' Type: ' + self.type

class ClusterProject(models.Model):
    """An openstack project that a user has access to.
       Currently a workaround because keystone doesn't
       have list_projects for a non-admin in our
       policy file
    """
    name = models.CharField(max_length=DEFAULT_FIELD_LEN)
    token = models.TextField(default=None, blank=True, null=True)

    ## Link to a cluster    
    #cluster = models.ForeignKey(Cluster)
    ## UI Project that the ClusterProject is attached to
    #ui_project = models.ForeignKey(UIProject)
    ## Associate services with the ClusterProject
    service = models.ManyToManyField(Service, through = 'ClusterProject_service')

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
                client = keystoneclient.Client(user_name=self.cluster_account.cluster_user_name,
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
        return novaclient.Client(self.cluster_account.cluster_user_name,
                                 self.cluster_account.cluster_password,
                                 self.name,
                                 self.cluster_account.cluster.auth_url)

class ClusterProject_service(models.Model):
    default = models.BooleanField(default = False)
    project = models.ForeignKey(ClusterProject)
    service = models.ForeignKey(Service)

    def __unicode__(self):
        return self.service.image_name

