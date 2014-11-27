from auth import nova, keystone

def listVMs():
	vms = []
	server_list = nova.servers.list()
	for server in server_list:
		vm = {
		'name':server.name,
		'desc':server.id,
 		'status':server.status,
 		'image':server.image[u'id'],
 		'network':server.networks[u'private'][0]
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


def create(): 
	name = raw_input('name: ')
	fl   = raw_input('flavor: ')  
	fl = nova.flavors.find(name='m1.'+fl)
	print(nova.servers.create(name, 'ed451e82-887b-42e1-b631-d28f46a5eed2',flavor=fl,meta=None,files=None))

def createDefault(VMname):
	fl = nova.flavors.find(name='m1.tiny')
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


