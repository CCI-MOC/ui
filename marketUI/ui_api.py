from settings import Nova

def list():
	vms = []
	server_list = Nova.servers.list(detailed=True)
	for server in server_list:
		vm = {'name':server.name, 'desc':server.id, 'status':server.status, 'image':server.image[u'id'], 'network':server.networks[u'private']}
		vms.append(vm)
	return vms
list()

def create(): 
	name = raw_input('name: ')
	fl   = raw_input('flavor: ')  
	fl = Nova.flavors.find(name='m1.'+fl)
	print(Nova.servers.create(name, 'ed451e82-887b-42e1-b631-d28f46a5eed2',flavor=fl,meta=None,files=None))


def delete(): 
	servers_list = Nova.servers.list()
	server_exists = False
        name = raw_input('name: ')
	for s in servers_list:
	    if s.name == name:
		print("This server %s exists" % name)
		server_exists = True
		break
	if not server_exists:
	    print("server %s does not exist" % name)
	else:
	    print("deleting server..........")
	    nova.servers.delete(s)
	    print("server %s deleted" % name)	

