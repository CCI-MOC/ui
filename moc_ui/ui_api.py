from auth import loginUser, loginTenant
from os import environ as env
import views
import time

def login(username, password, auth_url):
	"""
	Create keystone client for user
	"""
	global keystone
	keystone = loginUser(username, password, auth_url)

def joinTenant(username, password, tenantName, auth_url):
	"""
	Create keystone client for specified tenant;
	User's credentials already authenticated on login
	"""

        global keystone, nova, glance
        keystone, nova, glance = loginTenant(username, password, tenantName, auth_url)


#### VMs ####

def listVMs():
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
		    if u'private' in server.networks:
		        vm['network'] = server.networks[u'private']
		    else:
		        vm['network'] = 'no network'
		vms.append(vm)
	return vms

def listImages():
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

def listFlavors():
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

def createVM(VMname, imageName, flavorName):
	"""
	Create VM on current tenant with specified information
	"""
    image = nova.images.find(name=imageName)
	fl = nova.flavors.find(name=flavorName)
    nova.servers.create(VMname, image=image, flavor=fl, meta=None,files=None)

def createDefault(VMname):
	"""Previously used for testing"""
	fl = nova.flavors.find(name='m1.nano')
	image = nova.images.find(name='cirros-0.3.2-x86_64-uec-ramdisk')
	nova.servers.create(VMname, image=image, flavor=fl, meta=None,files=None)
	
def delete(VMname): 
	"""
	Delete specified VM from current tenant
	"""
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


## VM Control Functions ## 
## VM = VM.id ##

def editVM(VM, flavor):
	"""
	Attempt to resize specified VM
	Broken - needs confirmation of resize (after resize operation completion)
	"""
	nova.servers.resize(VM, flavor)
	#nova.servers.confirm_resize(VM)

def startVM(VM):
	nova.servers.start(VM)

def pauseVM(VM):
	nova.servers.pause(VM)

# Not yet implement / incorporated 
def unpauseVM(VM):
	nova.servers.unpause(VM)		
		
def stopVM(VM):
	nova.servers.stop(VM)
		

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
        tenant_list = keystone.tenants.list()
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


### User ###

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


