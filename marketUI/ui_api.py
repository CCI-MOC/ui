import settings

def list(): 

	nova = settings.Nova
	vms = []
	server_list = nova.servers.list()
	for server in server_list:
		vm = {'name': server.name,'image':server.image[u'id']}
		vms.append(vm)
	return vms

def create(): 
	#nova = Client('2', 'nova', 'admin', 'service', 'http://10.0.2.15:5000/v2.0')
	nova = settings.Nova
	name = raw_input('name: ')
	fl   = raw_input('flavor: ')  
	fl = nova.flavors.find(name='m1.'+fl)
	print(nova.servers.create(name, 'ed451e82-887b-42e1-b631-d28f46a5eed2',flavor=fl,meta=None,files=None))


import time

def delete(): 
	#nova = Client('2', 'nova', 'admin', 'service', 'http://10.0.2.15:5000/v2.0')
	nova = settings.Nova
	servers_list = nova.servers.list()
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

list()
