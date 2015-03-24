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
test_vm_list = [{'name': 'hadoop master', 'state': '=)', 'img': 'centOS 7'},
                {'name': 'hadoop slave 1', 'state': '=)', 'img': 'centOS 7'},
                {'name': 'hadoop slave 2', 'state': '=)', 'img': 'centOS 7'},
                {'name': 'web server', 'state': 'off', 'img': 'Ubuntu 14.10'},
                {'name': 'database', 'state': 'build', 'img': 'RHEL 7'},
                {'name': 'bad machine', 'state': '=(', 'img': 'Windows 8'}]

test_project_list = [{'name': 'Ahri', 'vm_list': test_vm_list}, 
                 {'name': 'Lucian', 'vm_list': test_vm_list}, 
                 {'name': 'YasuWoh', 'vm_list': test_vm_list},
                 {'name': 'bulbasour', 'vm_list': test_vm_list},
                 {'name': 'chardmonger', 'vm_list': test_vm_list}, 
                 {'name': 'link', 'vm_list': test_vm_list},
                 {'name': 'epona', 'vm_list': test_vm_list}, 
                 {'name': 'zelda', 'vm_list': test_vm_list}]

