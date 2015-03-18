from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import ui_api as api
import time
import forms 
import models 


### Login Page ###

def front_page(request):
    """
    Front page;
    Enter credentials to be processed by the login view 
    """
    login_buttons = [{'name': 'submit', 'type': 'submit', 'action': '/login/', 'class': 'btn-primary'},
                    {'name': 'sign-up', 'type': 'modal', 'data_target': '#createUser', 'class': 'btn-success'}]

    login_data = {'name': 'MOC Login =)', 'action': '/login', 'method': 'post', 'button_list': login_buttons}

    reg_modal = {'id': 'createUser', 'action': '/register', 'method': 'post', 'title': 'Register User'}

    login_form = forms.LoginForm()
    reg_form = forms.UserRegisterForm()

    return render(request, 'front_page.html', {'OCXlogin': 'OCXi', 'login_data': login_data, 
        'login_form': login_form, 'reg_modal': reg_modal, 'reg_form': reg_form})

def login(request):
    """
    Login view;
    Checks post credentials, redirects to projects or back to front page with error
    """
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                user = models.User.objects.get(name=username)
                if user.verify_password(password=password):
                    request.session['username'] = username
                    return HttpResponseRedirect('/projects')
            except:
                pass
        
    return HttpResponseRedirect('/')

def logout(request):
    """
    Logout of session; 
    remove session variables and return to login page
    """
    for state, sessionInfo in request.session.items():
        sessionInfo = None
    return HttpResponseRedirect('/')

def register(request):
    """
    Register new user with keystone; called from login page
    Needs error checking
    """
    if request.method == "POST":
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_exist = models.User.objects.filter(name=username)

            if 'pk' not in user_exist:
                newuser = models.User(name=username)
                newuser.set_password(password=password)
                newuser.save()
                request.session['username'] = username
                return HttpResponseRedirect('/projects/')

    return HttpResponseRedirect('/')

def clusters(request):
    """
    List keystone projects available to the user; 
    attempt to login with credentials
    """
    test_cluster_list = [{name: 'pokemans cluster', projects: [{'name': 'bulbasour', 'url': '/projects/'},
	   						       {'name': 'chardmonger', 'url': '/projects/'},] }
	   						       {'name': 'squirtle squirt', 'url': '/projects/'},] }
			{name: 'TMNT cluster', projects: [{'name': 'leodizzle'},{}] }
  						       {'name': 'chardmonger', 'url': '/projects/'},] }
						       {'name': 'squirtle squirt', 'url': '/projects/'},] }

		    ] 
        
       # pass session's user info to keystone for authentication
       #     api.login(request.session['username'], request.session['password'], request.session['auth_url'])
       #     projects = api.listTenants()
    return render(request, 'projects.html', {'user_projects': projects})

### Projects Page ###

def projects(request):
    """
    List keystone projects available to the user; 
    attempt to login with credentials
    """
    test_cluster_list = {}
    test_project_list = {}
        
       # pass session's user info to keystone for authentication
       #     api.login(request.session['username'], request.session['password'], request.session['auth_url'])
       #     projects = api.listTenants()
    return render(request, 'projects.html', {'user_projects': projects})

def enterProject(request):
    """
    Called when a tenant is chosen on Projects page; 
    attempt to enter tenant via keystone
    """
    if request.method == 'POST':
        form = forms.TenantLoginForm(request.POST)
        if form.is_valid():
            tenantName = form.cleaned_data['tenantName']
            request.session['tenant'] = tenantName
            tenantID = form.cleaned_data['tenantID']
            
            # send session user/pw and selected tenant to keystone
            api.joinTenant(request.session['username'], request.session['password'], tenantName, request.session['auth_url'])
            return HttpResponseRedirect('/project_space/manage')
    print('Invalid User')
    return HttpResponseRedirect('/projects/')

def createProject(request):
    """
    Create new project from Projects page
    """
    if request.method == 'POST':
        form = forms.TenantCreateForm(request.POST)
        if form.is_valid():
            projectName = form.cleaned_data['tenantName']
            projectDesc = form.cleaned_data['tenantDesc']
            
            # work around for user to have project creation privileges
            # for some reason, unable to create a project unless
            # keystone client is passed a tenant_name arguement; can't create solely as user
            api.joinTenant('admin', 'admin', 'demo')
            # create project with current keystone session
            api.createTenant(projectName, projectDesc)
            # add user to new project with admin role
            api.addUser(request.session['username'], 'admin', projectName)      

    print ('Unable to create new Project')
    return HttpResponseRedirect('/projects')


### Marketplace Page ###

def market(request):
    """
    Marketplace page; hardcoded values
    """
    resources = [
        {'name': 'Hadoop','desc':'Hadoop as a Service', 'tag': 'service', 'icon': 'http://cdn.blog-sap.com/innovation/files/2012/09/hadoop-elephant.jpg'},
        {'name': 'Wireshark','desc':'Wireshark Appliance', 'tag': 'appliance', 'icon': 'http://halozatbiztonsag.hu/sites/default/files/WireShark_2.png'},
        {'name': 'NGINX','desc':'NGINX Loadbalancer Appliance', 'tag': 'appliance', 'icon': 'http://shailan.com/wp-content/uploads/nginx-logo-1.png'},
        {'name': 'BU-Compute','desc':'BU Computing', 'tag': 'compute', 'icon': 'http://www.openstack.org/themes/openstack/images/new-icons/openstack-compute-icon.png'},
        {'name': 'HU-Storage','desc':'HU Storage', 'tag': 'storage', 'icon': 'http://openstack.org//themes/openstack/images/new-icons/openstack-object-storage-icon.png'} ]
    return render(request, 'market.html', {'market': resources})


###Project Management Page###

def manage(request):
    """
    Project Management page; edit VMs, project settings
    """
    if request.method == 'POST':
        form = forms.VMCreateForm(request.POST)
        if form.is_valid():
            VMname = form.cleaned_data['newVM']
            image = form.cleaned_data['imageName']
            flavor = form.cleaned_data['flavorName']
            return HttpResponseRedirect('/project_space/manage/create/'+VMname+';'+image+';'+flavor)    

    # temporary fix to ensure user stays connected to current project
    api.joinTenant(request.session['username'], request.session['password'], request.session['tenant'], request.session['auth_url'])
    VMs = api.listVMs()
    images = api.listImages()
    flavors = api.listFlavors()
    return render(request, 'manage.html', {'project_VMs':VMs, 
                  'images':images, 'flavors':flavors, 
                  'tenant':request.session['tenant']})

def deleteVM(request, VMname):
    """
    Delete selected VM; called from editVM modal
    """
    api.delete(VMname)
    return HttpResponseRedirect('/project_space/manage')

def createVM(request, VMname, imageName, flavorName):
    """
    Create VM with specified fields; from createVM modal
    """
    api.createVM(VMname, imageName, flavorName)
    return HttpResponseRedirect('/project_space/manage')

def createDefaultVM(request, VMname):
    """Unused; previously for testing"""
    api.createDefault(VMname)
    return HttpResponseRedirect('/project_space/manage')

def edit(request):
    """
    EditVM modal (pop up); retrieves VM/flavor IDs
    """
    if request.method == 'POST':
        form = forms.VMEditForm(request.POST)
        if form.is_valid():
            VM_id = form.cleaned_data['VM_id']
            flavor_id = form.cleaned_data['flavor_id']  
            api.editVM(VM_id, flavor_id)
            return HttpResponseRedirect('/project_space/manage')
    else:
        return HttpResponseRedirect('/project_space/manage')

def editControlVM(request):
    """
    EditVM modal footer; submission of VM controlling actions
    """
    if request.method == 'POST':
        form = forms.VMControlForm(request.POST)
        if form.is_valid():
            VM_id = form.cleaned_data['VM_id']
            if(form.cleaned_data['action'] == 'start'):
                api.startVM(VM_id)
            elif(form.cleaned_data['action'] == 'pause'):
                api.pauseVM(VM_id)
            elif(form.cleaned_data['action'] == 'stop'):
                api.stopVM(VM_id)
    return HttpResponseRedirect('/project_space/manage')


### Project Settings ###

def settings(request):
    """
    Project Settings; ADMIN ONLY; 
    add/edit/delete current tenant's users
    """
    # work around lack of keystone session; recreate keystone client on page arrival
    api.joinTenant(request.session['username'], request.session['password'], request.session['tenant'], request.session['auth_url'])
    tenant = api.getTenant(request.session['tenant'])
    users = api.listUsers(tenant)
    return render(request, 'settings.html', {'tenant': tenant.name, 'users': users})

def deleteProject(request, projectName):
    """
    Delete current project
    """
    api.deleteTenant(projectName)
    return HttpResponseRedirect('/projects')

def addUser(request, projectName):
    """
    Add user to current project
    """
    if request.method == "POST":
        form = forms.UserAddForm(request.POST)
        if form.is_valid():
            # recreate keystone client; keystone session work around
            api.joinTenant(request.session['username'], request.session['password'], projectName, request.session['auth_url'])
            api.addUser(form.cleaned_data['userName'], form.cleaned_data['roleName'], projectName)
        return HttpResponseRedirect('/project_space/manage/settings')

def editRole(request):
    """
    Add role to selected user for current project
    """
    if request.method == "POST":
        form = forms.RoleEditForm(request.POST)
        if form.is_valid():
            # recreate keystone client; keystone session work around
            api.joinTenant(request.session['username'], request.session['password'], request.session['tenant'], request.session['auth_url'])
            if form.cleaned_data['editAction'] == 'add':
                api.addRole(form.cleaned_data['userName'], form.cleaned_data['roleName'], request.session['tenant'])
            elif form.cleaned_data['editAction'] == 'remove':
                api.removeUserRole(form.cleaned_data['userName'], form.cleaned_data['roleName'], request.session['tenant'])
        return HttpResponseRedirect('/project_space/manage/settings')

def removeUser(request):
    """
    Remove user from current project
    """
    if request.method == "POST":
        form = forms.UserRemoveForm(request.POST)
        if form.is_valid():
            # recreate keystone client; keystone session work around
            api.joinTenant(request.session['username'], request.session['password'], projectName, request.session['auth_url'])
            api.removeUser(form.cleaned_data['userName'], form.cleaned_data['roleName'], projectName)
        return HttpResponseRedirect('/project_space/manage/settings')

# Misc.
def modal(request):
    options = [
        {'compute': 'small'},
        {'storage': 'BU'},
        {'network': 'private'}]
    return render(request, 'modal.html', {'options': options})
