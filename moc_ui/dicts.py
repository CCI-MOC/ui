import forms
## SAMPLE
sample_buttons = [{'name': 'NAME', 'type': 'BUTTON-TYPE', 'action': '/URL/', 'class': 'btn-primary'},]

sample_form_data = {'name': 'TITLE', 'action': '/URL', 'method': 'post', 'button_list': sample_buttons} 

sample_modal = {'id': 'createUser', 'action': '/register', 'method': 'post', 'title': 'Register User'} 

## FRONT PAGE
login_buttons = [{'name': 'log in', 'type': 'submit', 'action': '/login/', 'class': 'btn-primary'}, 
                 {'name': 'sign up', 'type': 'modal', 'data_target': '#createUser', 'class': 'btn-success'}] 

login_data = {'name': 'MassOpenCloud Login', 'action': '/login', 'method': 'post', 'button_list': login_buttons} 

reg_modal = {'id': 'createUser', 'action': '/register', 'method': 'post', 'title': 'Register User'} 


# CLOUDS PAGE
test_vm_list_1 = [{'name': 'hadoop master', 'state': '=)', 'provider': 'HU-prod', 'image': 'centOS 7'},
                {'name': 'hadoop slave 1', 'state': '=)', 'provider': 'BU-prod', 'image': 'centOS 7'},
                {'name': 'hadoop slave 2', 'state': '=)', 'provider': 'NE-prod', 'image': 'centOS 7'},
                {'name': 'hadoop slave 2', 'state': 'build', 'provider': 'UMASS-prod', 'image': 'centOS 7'},
                {'name': 'hadoop slave 3', 'state': 'off', 'provider': 'HU-dev', 'image': 'centOS 7'},
                {'name': 'bad machine', 'state': '=(', 'provider': 'MIT-dev', 'image': 'Windows 8'}]

test_vm_list_2 = [{'name': 'web server', 'state': '=)', 'provider': 'HU-prod', 'image': 'Ubuntu 14.10'},
                {'name': 'database', 'state': 'build', 'provider': 'HU-dev', 'image': 'Suse'},]

test_project_list = [{'name': 'big_data', 'vm_list': test_vm_list_1}, 
                     {'name': 'webservers', 'vm_list': test_vm_list_2}]


# MARKET PAGE

test_market_list = [
                    {'name':'Red Hat','img_url':'/static/redhat-logo.png','provider':'redhat','description':'PostgreSQL', 'version':'9.1', 'availability':'Yes', 'type':'Support', 'image':'centOS 7'},
                    {'name':'Dell','img_url':'/static/Dell.png','provider':'Dell','description':'Dell Compute', 'version':'3.1.4', 'availability':'Yes', 'type':'Compute', 'image':'centOS 7'},
                    {'name':'Lenovo','img_url':'/static/lenovo-logo.jpg','provider':'Lenovo','description':'Lenovo Compute', 'version':'3.1.4', 'availability':'Yes', 'type':'Compute', 'image':'centOS 7'},
                    #{'name':'HP','img_url':'/static/HP.png','provider':'HP','description':'HP Compute', 'version':'3.1.4', 'availability':'Yes', 'type':'Compute', 'image':'centOS 7'},
                    {'name':'Intel','img_url':'/static/intel.png','provider':'Intel','description':'Intel Compute', 'version':'3.1.4', 'availability':'Yes', 'type':'Compute', 'image':'centOS 7'},
                    {'name':'Brocade', 'img_url':'/static/Brocade.png','provider':'Brocade','description':'Brocade Networking', 'version':'3.1.4', 'availability':'Yes', 'type':'Network', 'image':'centOS 7'},
                    {'name':'Fujitsu','img_url':'/static/fujitsu-logo.jpg','provider':'Fujitsu','description':'Fujitsu Storage', 'version':'3.1.4', 'availability':'Yes', 'type':'Storage', 'image':'centOS 7'},
                    {'name':'EMC','img_url':'/static/EMC.jpg','provider':'EMC','description':'EMC Storage', 'version':'3.1.4', 'availability':'Yes', 'type':'Storage', 'image':'centOS 7'},
                    {'name':'Juniper','img_url':'/static/Juniper.png','provider':'Juniper','description':'Juniper Networking', 'version':'3.1.4', 'availability':'Yes', 'type':'Network', 'image':'centOS 7'},
                    {'name':'Cisco','img_url':'/static/Cisco.jpeg','provider':'Cisco','description':'Cisco Networking', 'version':'3.1.4', 'availability':'Yes', 'type':'Network', 'image':'centOS 7'},
                    #{'name':'OpenShift','img_url':'/static/OpenShift.jpg','provider':'RedHat','description':'OpenShift PaaS', 'version':'1.0.0', 'availability':'Yes', 'type':'Application', 'image':'centOS 7'},
                    {'name':'Hadoop','img_url':'/static/hadoop.jpg','provider':'Apache','description':'Apache Hadoop', 'version':'2.6.0', 'availability':'Yes', 'type':'Application', 'image':'centOS 7'},
                    {'name':'NetApp','img_url':'/static/Netapp.png','provider':'NetApp','description':'NetApp Storage', 'version':'3.1.4', 'availability':'Yes', 'type':'Storage', 'image':'centOS 7'},
                    {'name':'PostgreSQL','img_url':'/static/Postgre.jpg','provider':'Postgre','description':'PostgreSQL', 'version':'9.1', 'availability':'Yes', 'type':'Application', 'image':'centOS 7'}]

# USER PAGE
test_user_list = [{'name': 'Alex', 'role_list': "admin"}, 
                     {'name': 'Bill', 'role_list': "member"},
                     {'name': 'Jon', 'role_list': "partner"},
                     {'name': 'Lucas', 'role_list': "member"},
                     {'name': 'Thomas', 'role_list': "admin"}]

