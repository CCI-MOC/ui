from os import environ as env

# Client package
#import novaclient.v1_1.client as nvclient

#from novaclient import client as nvclient

#import glanceclient.v2.client as glclient
#import keystoneclient.v2_0.client as ksclient

# from keystoneclient.auth.identity import v2

from keystoneauth1.identity import v3

from keystoneauth1 import session

from keystoneclient.v3 import client as ksclient
from novaclient import client as nvclient
from glanceclient import client as glclient

# Socks
#import socks
#import socket

# Set up SOCKS proxy usage:
#s = socks.socksocket()

# Set up the Port number as the one used for connecting Harvard Cluster
#socks.set_default_proxy(socks.SOCKS5, 'localhost', 5507)
#socket.socket = socks.socksocket

# Log User to his/her associated Tenant 
def loginTenant(request, tenant_name):
	"""
	Create keystone, nova, and glance clients for tenant; on tenant selection
	"""

	username = request.session['username']
	password = request.session['password']
	auth_url = 'https://engage1.massopencloud.org:5000/v3/'
	
	print 'lucas-test-auth-loginTenant'
	
	unscoped_auth = v3.Password(auth_url = auth_url, username = username, password = password, user_domain_name="Default", unscoped=True)
	unscoped_sess=session.Session(auth=unscoped_auth)
	unscoped_token=unscoped_sess.get_token()
	auth=v3.Token(auth_url = auth_url,token=unscoped_token)
	sess=session.Session(auth=auth)
	#scoped_token=sess.get_token()
	keystone = ksclient.Client(session=sess)
	# keystone = ksclient.Client(auth_url = 'https://engage1.massopencloud.org:5000/v2.0/', username = username,
	# 	password = password, tenant_name = tenant_name)
	print 'lucas-test-auth-loginTenant-succesfully'
	# nova = nvclient.Client('2', auth_url = 'https://engage1.massopencloud.org:5000/v2.0/',
	# 	username = username,
	# 	api_key = password,
	# 	project_id = tenant_name)
	nova = nvclient.Client('2', session=sess)
	glance = glclient.Client('2', session=sess)
	return {'keystone': keystone, 'nova': nova, 'glance': glance}

def get_keystone(request, tenant_name):
	username = request.session['username']
	password = request.session['password']
	auth_url = 'https://engage1.massopencloud.org:5000/v3/'
	# keystone = ksclient.Client(auth_url = 'https://engage1.massopencloud.org:5000/v2.0/', username = username,
	# 	password = password, tenant_name = tenant_name)
	unscoped_auth = v3.Password(auth_url = auth_url, username = username, password = password, user_domain_name="Default", unscoped=True)
	unscoped_sess=session.Session(auth=unscoped_auth)
	unscoped_token=unscoped_sess.get_token()
	auth=v3.Token(auth_url = auth_url,token=unscoped_token)
	sess=session.Session(auth=auth)
	#scoped_token=sess.get_token()
	keystone = ksclient.Client(session=sess)
	return keystone

def get_nova(request, tenant_name):
	username = request.session['username']
	password = request.session['password']
	auth_url = 'https://engage1.massopencloud.org:5000/v3/'

	unscoped_auth = v3.Password(auth_url = auth_url, username = username,
		password = password, user_domain_name="Default", unscoped=True)
	unscoped_sess=session.Session(auth=unscoped_auth)
	unscoped_token=unscoped_sess.get_token()
	auth=v3.Token(auth_url = auth_url,token=unscoped_token)
	sess=session.Session(auth=auth)
	nova = nvclient.Client('2', session=sess)
	# nova = nvclient.Client('2', auth_url = 'https://engage1.massopencloud.org:5000/v2.0/',
	# 	username = username,
	# 	api_key = password,
	# 	project_id = tenant_name)
	return nova

def get_glance(request, tenant_name):
	username = request.session['username']
	password = request.session['password']
	auth_url = 'https://engage1.massopencloud.org:5000/v3/'

	# keystone = get_keystone(request,tenant_name)
	# nova = get_nova(request,tenant_name)
	unscoped_auth = v3.Password(auth_url = auth_url, username = username,
		password = password, user_domain_name="Default", unscoped=True)
	unscoped_sess=session.Session(auth=unscoped_auth)
	unscoped_token=unscoped_sess.get_token()
	auth=v3.Token(auth_url = auth_url,token=unscoped_token)
	sess=session.Session(auth=auth)
	glance = glclient.Client('2', session=sess)
	return glance
	


# def loginUser(username, password, request):
#         """
# 	Create keystone client for user; called on login
# 	"""
# 	print 'lucas-test-auth-loginUser'
	
#         keystone = ksclient.Client(
# 	        auth_url = 'https://engage1.massopencloud.org:5000/v2.0/',
# 		username = username,
#        		password = password)
#     	print 'lucas-test-auth-loginUser-succesfully'
# 	return keystone


# def _loginTenant (request, username, password, tenant_name):
# 	auth_url = 'https://engage1.massopencloud.org:5000/v2.0/'
# 	auth = v2.Password(auth_url = auth_url, username = username, password = password, tenant_name = tenant_name)
# 	sess = session.Session(auth=auth)
# 	nova = client.Client('1.1', session=sess)


