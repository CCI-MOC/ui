## SAMPLE
sample_buttons = [{'name': 'NAME', 'type': 'BUTTON-TYPE', 'action': '/URL/', 'class': 'btn-primary'},]

sample_form_data = {'name': 'TITLE', 'action': '/URL', 'method': 'post', 'button_list': sample_buttons} 

sample_modal = {'id': 'createUser', 'action': '/register', 'method': 'post', 'title': 'Register User'} 

## FRONT PAGE
login_buttons = [{'name': 'submit', 'type': 'submit', 'action': '/login/', 'class': 'btn-primary'}, 
                 {'name': 'sign-up', 'type': 'modal', 'data_target': '#createUser', 'class': 'btn-success'}] 

login_data = {'name': 'MassOpenCloud Login =)', 'action': '/login', 'method': 'post', 'button_list': login_buttons} 

reg_modal = {'id': 'createUser', 'action': '/register', 'method': 'post', 'title': 'Register User'} 


# CLOUDS PAGE
test_vm_list = [{'name': 'vm1', 'state': 'on', 'img': 'ubuntu'},
                {'name': 'vm2', 'state': 'off', 'img': 'centos7'},
                {'name': 'vm3', 'state': 'build', 'img': 'RHEL7'},
                {'name': 'vm4', 'state': 'error', 'img': 'Windows 8'}]

test_cloud_list = [{'name': 'Harvard Production', 'projects': [{'name': 'Ahri', 'vm_list': test_vm_list}, 
                                                               {'name': 'Lucian', 'vm_list': test_vm_list}, 
                                                               {'name': 'YasuWoh', 'vm_list': test_vm_list}]},
                   {'name': 'Harvard Development', 'projects': [{'name': 'bulbasour', 'vm_list': test_vm_list},
                                                                {'name': 'chardmonger', 'vm_list': test_vm_list}, 
                                                                {'name': "picka - ha'choo", 'vm_list': test_vm_list}, 
                                                                {'name': 'squirtle squirt', 'vm_list': test_vm_list}]},
                   {'name': 'Amazon EC2', 'projects': [{'name': 'link', 'vm_list': test_vm_list},
                                                       {'name': 'epona', 'vm_list': test_vm_list}, 
                                                       {'name': 'zelda', 'vm_list': test_vm_list},]}]


league_cloud = {}
cloud_buttons = {} 
create_cloud_modal = {'id': 'createUser', 'action': '/register', 'method': 'post', 'title': 'Register User'}
