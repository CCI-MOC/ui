from os import environ as env
import novaclient.v1_1.client as nvclient
import glanceclient.v2.client as glclient
import keystoneclient.v2_0.client as ksclient

# admin keystone auth
keystone = ksclient.Client(token='admin', endpoint='http://10.0.2.15:35357/v2.0/')

#glance_endpoint = keystone.service_catalog.url_for(service_type='image')
#glance = glclient.Client(glance_endpoint, token=keystone.auth_token)

nova = nvclient.Client(auth_url=env['OS_AUTH_URL'],
username=env['OS_USERNAME'],
api_key=env['OS_PASSWORD'],
project_id=env['OS_TENANT_NAME'],
region_name=env['OS_REGION_NAME'])

