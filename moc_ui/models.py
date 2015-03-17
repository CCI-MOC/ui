from django.db import models
from passlib.hash import sha512_crypt

# Lengths for CharField, as it is required
PASSHASH_LEN = len(sha512_crypt.encrypt(''))
DEFAULT_FIELD_LEN = 255 


class User(models.Model):
     """A user of the marketplace UI"""
     name = models.CharField(max_length=DEFAULT_FIELD_LEN)
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
     auth_endpoint = models.URLField()
    
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
