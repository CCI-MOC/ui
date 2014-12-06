from auth import keystone, nova, glance, loginUser, loginTenant
from os import environ as env
import views
import time


# Uses admin authenticated keystone, nova, and glance by default
def login(username, password):
	global keystone
	keystone = loginUser(username, password)

def joinTenant(username, password, tenantName):
        global keystone, nova, glance
        keystone, nova, glance = loginTenant(username, password, tenantName)


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
 		'network':'-',
		'vnc':server.get_vnc_console('novnc')[u'console'][u'url']
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
	"""Previously used for testing"""
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

# VM Control Functions; VM = VM.id
def editVM(VM, flavor):
	nova.servers.resize(VM, flavor)
	#nova.servers.confirm_resize(VM)

def startVM(VM):
	nova.servers.start(VM)

def pauseVM(VM):
	nova.servers.pause(VM)

# needs to be incorporated
def unpauseVM(VM):
	nova.servers.unpause(VM)		
		
def stopVM(VM):
	nova.servers.stop(VM)
		

### Tenant ###

def getTenant(tenantName):
	tenants = keystone.tenants.list()
	for tenant in tenants:
		if tenant.name == tenantName:
			return tenant
	return 'Unable to find Current Tenant'

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

def createTenant(name, description):
	keystone.tenants.create(
		tenant_name = name,
		description = description,
		enabled = True)

def deleteTenant(tenantName):
	tenants = keystone.tenants.list()
	tenant = [x for x in tenants if x.name==tenantName][0]
	keystone.tenants.delete(tenant)	


### User ###

def addUser(userName, roleName, tenantName):
	"""Adds a user to a tenant with specified role"""
	users = keystone.users.list()
	user = [x for x in users if x.name==userName][0]
	roles = keystone.roles.list()
	role = [x for x in roles if x.name==roleName][0]
	tenants = keystone.tenants.list()
	tenant = [x for x in tenants if x.name==tenantName][0]
	keystone.roles.add_user_role(user, role, tenant)
	

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


