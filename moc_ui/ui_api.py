from auth import  loginTenant, get_nova, get_keystone, get_glance
from os import environ as env
import views
import time


def login(username, password, request):
	print 'lucas-test-ui-api-login'
	"""
	Create keystone client for user
	"""
	global keystone
	keystone = loginUser(username, password, request)

def joinTenant(request, tenant_name):
	"""
	Create keystone client for specified tenant;
	User's credentials already authenticated on login
	"""
        return loginTenant(request = request, tenant_name = tenant_name)
 

#### VMs ####

def listVMs(nova):
	"""
	Gather and list VMs' info for current tenant
	"""
	
	vms = []
	server_list = nova.servers.list()
	network = nova.networks.list()
	print network
	for server in server_list:
		vm = {
		'name':server.name,
		'id':server.id,
 		'status':server.status,
 		'image':nova.images.get(server.image[u'id']).name,
		'flavor':nova.flavors.get(server.flavor[u'id']).name,
 		'network':'-',
		'vnc':'-'
		}
		'''
		if server.status != 'BUILD':
			vm['vnc'] = server.get_vnc_console('novnc')[u'console'][u'url']
			vm['network'] = server.networks[u'private']
		'''
		vms.append(vm)
	return vms



def _listVMs():
	"""
	Gather and list VMs' info for current tenant
	"""
	vms = []
	server_list = nova.servers.list()
	for server in server_list:
		vm = {
		'name':server.name,
		'id':server.id,
 		'status':server.status,
 		'image':nova.images.get(server.image[u'id']).name,
		'flavor':nova.flavors.get(server.flavor[u'id']).name,
 		'network':'-',
		'vnc':'-'
		}
		if server.status != 'BUILD':
			vm['vnc'] = server.get_vnc_console('novnc')[u'console'][u'url']
			vm['network'] = server.networks[u'private']
		vms.append(vm)
	return vms

def listImages(glance):
	"""
	List images available to current tenant
	"""
	images = []
        image_list = list(glance.images.list())
        for imageObj in image_list:
                image = {
		'name':imageObj.name,
		'id':imageObj.id
		}
                images.append(image)
        return images

def listFlavors(nova):
	"""
	List flavors available to current tenant
	"""
	flavors = []
	flavor_list = nova.flavors.list()
	for flavorObj in flavor_list:
		flavor = {
		'name': flavorObj.name,
		'id': flavorObj.id
		}
		flavors.append(flavor)
	return flavors

def createVM(nova, VMname, imageName, flavorName):
	"""
	Create VM on current tenant with specified information
	"""
        image = nova.images.find(name=imageName)
	fl = nova.flavors.find(name=flavorName)
	nics = [{"net-id": nova.networks.list()[0].id, "v4-fixed-ip": ''}]
        nova.servers.create(VMname, image=image, flavor=fl, meta=None, files=None, nics=nics)

def createDefault(nova):
	fl = nova.flavors.find(name='m1.small')
	image = nova.images.find(name='cirros-default')
	nics = [{"net-id": nova.networks.list()[0].id, "v4-fixed-ip": ''}]
	nova.servers.create("new_VM", image=image, flavor=fl, meta=None, files=None, nics=nics)
	
#delete VM
def delete(nova, VMid): 
	
	#find server
	servers_list = nova.servers.list()
	server_exists = False
	for s in servers_list:
	    if s.id == VMid:
		print("This server %s exists" % VMid)	#DEBUG
		server_exists = True
		break

	#delete server
	if not server_exists:
	    print("server %s does not exist" % VMid)	#DEBUG
	else:
	    print("deleting server..........")		#DEBUG
	    nova.servers.delete(s)
	    print("server %s deleted" % VMid)		#DEBUG


## VM Control Functions ## 
## VM = VM.id ##

def editVM(nova, VM, flavor):
	"""
	Attempt to resize specified VM
	Broken - needs confirmation of resize (after resize operation completion)
	"""
	nova.servers.resize(VM, flavor)
	#nova.servers.confirm_resize(VM)

#power up VM
def startVM(nova, VM):
	nova.servers.start(VM)

#shutdown VM
def stopVM(nova, VM):
	nova.servers.stop(VM)

#pause/unpause VM
def VM_active_state_toggle(nova, VMid):
	if nova.servers.get(VMid).status == u'PAUSED':
		nova.servers.unpause(VMid)
	elif nova.servers.get(VMid).status == u'ACTIVE':
		nova.servers.pause(VMid)
	else:
		pass



# Commenting useless stuff. We don't have the permission to do this 
# + future keystone changes will render any implementation of such pointless. 
		
'''
### Tenant ###

def getTenant(tenantName):
	"""
	Return tenant object of specified tenantName
	"""
	tenants = keystone.tenants.list()
	for tenant in tenants:
		if tenant.name == tenantName:
			return tenant
	return 'Unable to find Current Tenant'

def listTenants():
	"""
	Display list of tenants;
	per user's keystone client, only shows tenants user is a member of
	"""

        projects = []
        print 'lucas-test-ui-api-list-tenants'
        tenant_list = keystone.tenants.list()
        print 'lucsa-test-retreive-list'
        for tenant in tenant_list:
                project = {
                'name':tenant.name,
                'desc':tenant.description,
                'id':tenant.id
                }
                projects.append(project)
        return projects

def createTenant(name, description):
	"""
	Create a new tenant with given name, description
	"""
	keystone.tenants.create(
		tenant_name = name,
		description = description,
		enabled = True)

def deleteTenant(tenantName):
	"""
	Delete the specified tenant
	"""
	tenants = keystone.tenants.list()
	tenant = [x for x in tenants if x.name==tenantName][0]
	keystone.tenants.delete(tenant)	
'''

### User ###

'''
def addUser(userName, roleName, tenantName):
	"""
	Adds a user to a tenant with specified role via keystone
	"""
	users = keystone.users.list()
	user = [x for x in users if x.name==userName][0]
	roles = keystone.roles.list()
	role = [x for x in roles if x.name==roleName][0]
	tenants = keystone.tenants.list()
	tenant = [x for x in tenants if x.name==tenantName][0]
	tenant.add_user(user, role)

def deleteUser(userName):
	"""
	Adds a user to a tenant with specified role via keystone
	"""
	users = keystone.users.list()
	user = [x for x in users if x.name==userName][0]
	user.delete()

def addRole(userName, roleName, tenantName):
	"""
	Adds a role to specified user in current tenant
	"""
	users = keystone.users.list()
	user = [x for x in users if x.name==userName][0]
	roles = keystone.roles.list()
	role = [x for x in roles if x.name==roleName][0]
	tenants = keystone.tenants.list()
	tenant = [x for x in tenants if x.name==tenantName][0]
	keystone.roles.add_user_role(user, role, tenant=tenant)

def removeUserRole(userName, roleName, tenantName):
	"""
	Remove role from user for current tenant
	"""
	users = keystone.users.list()
	user = [x for x in users if x.name==userName][0]
	roles = keystone.roles.list()
	role = [x for x in roles if x.name==roleName][0]
	tenants = keystone.tenants.list()
	tenant = [x for x in tenants if x.name==tenantName][0]
	tenant.remove_user(user, role)	

def registerUser(userName, password, email):
	"""
	Registers a new user with keystone
	"""
	keystone.users.create(userName, password=password, email=email)	

def users():
	"""
	Create list of All the users in the system
	"""
        users = []
        user_list = keystone.users.list()
        for member in user_list:
                roleNames = []
                user = {
                'name':member.name,
                'id':member.id,
                'enabled':member.enabled,
                'email':member.email,
                }
                users.append(user)
        return users

def listUsers(tenant):
	"""
	Create list of current tenant's users with relevant information, roles
	"""
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

'''
