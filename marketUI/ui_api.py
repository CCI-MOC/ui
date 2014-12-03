from auth import keystone, nova, glance
import time
from os import environ as env
import subprocess

#### VMs ####

def listVMs():
# taking only private networks; hardcoded
	vms = []
	server_list = nova.servers.list()
	for server in server_list:
		vm = {
		'name':server.name,
		'id':server.id,
 		'status':server.status,
 		'image':nova.images.get(server.image[u'id']).name,
		'flavor':nova.flavors.get(server.flavor[u'id']).name,
 		'network':'-'
		}
		if server.status != 'BUILD':
			vm['network'] = server.networks[u'private']
		vms.append(vm)
	return vms

def listImages():
	images = []
        image_list = list(glance.images.list())
        for imageObj in image_list:
                image = {
		'name':imageObj.name,
		'id':imageObj.id
		}
                images.append(image)
        return images

def listFlavors():
	flavors = []
	flavor_list = nova.flavors.list()
	for flavorObj in flavor_list:
		flavor = {
		'name': flavorObj.name,
		'id': flavorObj.id
		}
		flavors.append(flavor)
	return flavors

def createVM(VMname, imageName, flavorName):
        image = nova.images.find(name=imageName)
	fl = nova.flavors.find(name=flavorName)
        nova.servers.create(VMname, image=image, flavor=fl, meta=None,files=None)

def createDefault(VMname):
	fl = nova.flavors.find(name='m1.nano')
	image = nova.images.find(name='cirros-0.3.2-x86_64-uec-ramdisk')
	nova.servers.create(VMname, image=image, flavor=fl, meta=None,files=None)
	
def delete(VMname): 
	servers_list = nova.servers.list()
	server_exists = False
	for s in servers_list:
	    if s.name == VMname:
		print("This server %s exists" % VMname)
		server_exists = True
		break
	if not server_exists:
	    print("server %s does not exist" % VMname)
	else:
	    print("deleting server..........")
	    nova.servers.delete(s)
	    print("server %s deleted" % VMname)	

def editVM(VM, flavor):
	nova.servers.resize(VM, flavor)
	#nova.servers.confirm_resize(VM)

def startVM(VM):
	nova.servers.start(VM)

def pauseVM(VM):
	nova.servers.pause(VM)

def unpauseVM(VM):
	nova.servers.unpause(VM)		
		
def stopVM(VM):
	nova.servers.stop(VM)
		

### Tenant / User ###

def getTenant():
	tenants = keystone.tenants.list()
	for tenant in tenants:
		if tenant.name == env['OS_TENANT_NAME']:
			return tenant
	return 'Unable to find Current Tenant'

def getUser(username):
	user_list = keystone
	return keystone.users.get(user.id)

def listTenants():
        projects = []
        tenant_list = keystone.tenants.list()
        for tenant in tenant_list:
                project = {
                'name':tenant.name,
                'desc':tenant.description,
                'id':tenant.id
                }
                projects.append(project)
        return projects

def listUsers(tenant):
        users = []
        user_list = tenant.list_users()
        for member in user_list:
                roleNames = []
                user = {
                'name':member.name,
                'id':member.id,
                'enabled':member.enabled,
                'email':member.email,
                'roles':roleNames
                }
                roles = member.list_roles(tenant=tenant.id)
                for role in roles:
                        roleNames.append(role.name)
                users.append(user)
        return users

def validUser(username, tenantID):
	tenant = keystone.tenants.get(tenantID)
	user_list = tenant.list_users()
	for user in user_list:
		if username == user.name:
			return True
	return False

def shell_source(script):
    """Sometime you want to emulate the action of "source" in bash,
    settings some environment variables. Here is a way to do it."""
    import subprocess, os
    pipe = subprocess.Popen(". %s; env" % script, stdout=subprocess.PIPE, shell=True)
    output = pipe.communicate()[0]
    environ = dict((line.split("=", 1) for line in output.splitlines()))
    env.update(environ)

def joinTenant(username, password, tenantName):
#	shell_source('openrc '+username+' '+password+' '+tenantName)
	env['OS_USERNAME'] = username
	env['OS_PASSWORD'] = password
	env['OS_TENANT_NAME'] = tenantName

