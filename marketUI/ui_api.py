from auth import nova, keystone, glance

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
 		'network':server.networks[u'private']
		}
		vms.append(vm)
	return vms

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
	for flavor in flavor_list:
		flavors.append(flavor.name)
	return flavors

def getTenant():
# hardcoded to return first tenant
	tenants = keystone.tenants.list()
	return tenants[0]

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


