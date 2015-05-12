from os import environ as env

# Client package
import novaclient.v1_1.client as nvclient
import glanceclient.v2.client as glclient
import keystoneclient.v2_0.client as ksclient

# from keystoneclient.auth.identity import v2
from keystoneclient import session
from novaclient import client

# Socks
import socks
import socket

# Set up SOCKS proxy usage:
s = socks.socksocket()

# Set up the Port number as the one used for connecting Harvard Cluster
socks.set_default_proxy(socks.SOCKS5, 'localhost', 5507)
socket.socket = socks.socksocket

# Log User to his/her associated Tenant 
def loginTenant(request, tenant_name):
	"""
	Create keystone, nova, and glance clients for tenant; on tenant selection
	"""

	username = request.session['username']
	password = request.session['password']

	print 'lucas-test-auth-loginTenant'
	keystone = ksclient.Client(auth_url = 'http://140.247.152.207:5000/v2.0', username = username,
		password = password, tenant_name = tenant_name)
	print 'lucas-test-auth-loginTenant-succesfully'
	nova = nvclient.Client(auth_url = 'http://140.247.152.207:5000/v2.0',
		username = username,
		api_key = password,
		project_id = tenant_name)
	glance_endpoint = keystone.service_catalog.url_for(service_type='image')
	glance = glclient.Client(glance_endpoint, token = keystone.auth_token)
	return {'keystone': keystone, 'nova': nova, 'glance': glance}

def get_keystone(request, tenant_name):
	username = request.session['username']
	password = request.session['password']
	keystone = ksclient.Client(auth_url = 'http://140.247.152.207:5000/v2.0', username = username,
		password = password, tenant_name = tenant_name)
	return keystone

def get_nova(request, tenant_name):
	username = request.session['username']
	password = request.session['password']
	nova = nvclient.Client(auth_url = 'http://140.247.152.207:5000/v2.0',
		username = username,
		api_key = password,
		project_id = tenant_name)
	return nova

def get_glance(request, tenant_name):
	username = request.session['username']
	password = request.session['password']
	glance_endpoint = keystone.service_catalog.url_for(service_type='image')
	glance = glclient.Client(glance_endpoint, token = keystone.auth_token)
	return {'keystone': keystone, 'nova': nova, 'glance': glance}
	

# def loginUser(username, password, request):
#         """
# 	Create keystone client for user; called on login
# 	"""
# 	print 'lucas-test-auth-loginUser'
	
#         keystone = ksclient.Client(
# 	        auth_url = 'http://140.247.152.207:5000/v2.0',
# 		username = username,
#        		password = password)
#     	print 'lucas-test-auth-loginUser-succesfully'
# 	return keystone


# def _loginTenant (request, username, password, tenant_name):
# 	auth_url = 'http://140.247.152.207:5000/v2.0'
# 	auth = v2.Password(auth_url = auth_url, username = username, password = password, tenant_name = tenant_name)
# 	sess = session.Session(auth=auth)
# 	nova = client.Client('1.1', session=sess)


