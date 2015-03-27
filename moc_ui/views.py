from django.shortcuts import render
from django.http import HttpResponseRedirect
# Forms to use in pages
import forms
# Dictionaries to pass to template context
import dicts
# Models to access our db's tables
import models 

## helper functions
def retrieveUser(userName):
    try:
        return models.User.objects.get(name=userName)
    except: 
        return None 

### Template Pages ### 
def front_page(request): 
    """ Front page; Enter credentials to be processed by the login view """ 
    
    return render(request, 'front_page.html', 
                 {'login_data': dicts.login_data, 'login_form': forms.login(), 
                  'reg_modal': dicts.reg_modal, 'reg_form': forms.userRegister()}) 

def clouds(request): 
    """List projects and vms in user's clouds""" 
    
    cloud_modals = [{'id': 'createProject', 'action': '/createProject', 'title': 'Create Project', 'form': forms.createProject()},
                    {'id': 'deleteProject', 'action': '/deleteProject', 'title': 'Delete Project', 'form': forms.deleteProject()},
                    {'id': 'createCluster', 'action': '/createCluster', 'title': 'Add Openstack Project', 'form': forms.createOSProject()},
                    {'id': 'deleteCluster', 'action': '/deleteCluster', 'title': 'Delete Openstack Project', 'form': forms.deleteOSProject()},
                    #{'id': 'createVM', 'title': 'Create VM', 'form': forms.createVM()},
                    {'id': 'deleteVM', 'action': '/deleteCluster', 'title': 'Delete VM', 'form': forms.deleteVM()},]
    createVMform = forms.createVM()

    user = retrieveUser(request.session['username'])

    try:
        projects = models.UIProject.objects.filter(user=user)
    except:
        pass

    project_list = []
    for project in projects:
        vm_list = []
        for vm in models.VM.objects.filter(ui_project=project):
            vm_list.append(vm.name)
        project_list.append({'name':project.name, 'vm_list': vm_list})

    for project in dicts.test_project_list:
        project_list.append(project)


    return render(request, 'clouds.html', {'project_list': project_list, 'cloud_modals': cloud_modals, 'createVMform': createVMform })

def market(request, project):
    market_list = []
    # for market in markets:
    #     market_choice_list = []
    #     for choice in dicts.test_

    for market in dicts.test_market_list:
        market_list.append(market)

    return render(request, 'market.html', 
            {'project': project, 'market_list': market_list})

### User Actions ###
def login(request):
    """ Login view; Checks post credentials, redirects
    to clouds or back to front page with error """
    if request.method == 'POST':
        form = forms.login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = retrieveUser(username)
            if user.verify_password(password=password):
                request.session['username'] = username
                return HttpResponseRedirect('/clouds')

    return HttpResponseRedirect('/')

def logout(request):
    """ Logout of session; remove session variables and return to login page """
    for state, sessionInfo in request.session.items():
        sessionInfo = None

    return HttpResponseRedirect('/')

def register(request):
    """ Register new user with keystone;
    called from login page Needs error checking """
    if request.method == "POST":
        form = forms.userRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = retrieveUser(username)
            if user is None:
                newuser = models.User(name=username)
                newuser.set_password(password=password)
                newuser.save()
                request.session['username'] = username
                return HttpResponseRedirect('/clouds')

    return HttpResponseRedirect('/')

## Project form processing
def createProject(request):
    """
    Process form to create a project, 
    if the project doesn't exist and user is registered,
    make new project in db
    """
    if request.method == "POST":
        form = forms.createProject(request.POST)
        if form.is_valid():
            print "form is valid"
            user = models.User.objects.get(name=request.session['username'])
            print user
            project_name = form.cleaned_data['name']
            print project_name

            try:
                project = models.UIProject(name=project_name, user=user)
                print project
            except:
                print "Error, project not made"
                project = None

            if project is not None:
                project.save()

    return HttpResponseRedirect('/clouds')

def deleteProject(request):
    """
    Process form to delete a project, 
    if the project doesn't exist and user is registered,
    make new project in db
    """
    if request.method == "POST":
        form = forms.deleteProject(request.POST)
        if form.is_valid():
            user = retrieveUser(request.session['username'])
            project_name = form.cleaned_data['name']

            try:
                project = models.UIProject.objects.get(name=project_name, user=user)
            except:
                project = None  

            if project is not None:
                project.delete()

    return HttpResponseRedirect('/clouds')

## cluster form processing
def createCluster(request):
    """
    Process form to create a cluster, 
    if the cluster doesn't exist and user is registered,
    make new cluster in db
    """
    if request.method == "POST": 
        form = forms.createCluster(request.POST) 
        if form.is_valid(): 
            user = retrieveUser(request.session['username'])
            cluster_name = form.cleaned_data['name'] 
            cluster_user_name = form.cleaned_data['user_name'] 
            cluster_password = form.cleaned_data['password'] 
            endpoint = form.cleaned_data['endpoint'] 

            try:
                cluster = models.Cluster(name=cluster_name, user_name=cluster_user_name, password=cluster_password, 
                                         endpoint=endpoint, user=user) 
            except:
                cluster = None

            if cluster is not None:
                cluster.save()

    return HttpResponseRedirect('/clouds')

def deleteCluster(request):
    if request.method == "POST": 
        form = forms.deleteCluster(request.POST)
        if form.is_valid():
            user = retrieveUser(request.session['username'])
            cluster_name = form.cleaned_data['name'] 
            action = form.cleaned_data['action']

            try:
                cluster = models.Cluster.objects.get(name=cluster_name, user=user) 
            except: 
                cluster = None 

            if cluster is not None:
                cluster.delete()

    return HttpResponseRedirect('/clouds') 
    
## vm form processing
def createVM(request):
    """Process form to create vm"""
    if request.method == "POST":
        form = forms.createVM(request.POST)
        if form.is_valid():
            user = retrieveUser(request.session['username'])
            vm_name = form.cleaned_data['name']
            OSProject = form.cleaned_data['cloud']
            try: 
                vm = models.VM.objects.get(name=vm_name, user=user)
            except:
                vm = None

            if vm is None:
                vm = models.VM(name=vm_name, user=user)
                vm.save()
    return HttpResponseRedirect('/clouds')

def deleteVM(request):
    """Process form to delete vm"""
    if request.method == "POST":
        form = forms.deleteVM(request.POST)
        if form.is_valid():
            user = retrieveUser(request.session['username'])
            vm_name = form.cleaned_data['name']

            try:
                vm = models.VM.objects.get(name=vm_name, user=user)
            except:
                vm = None

            if action == 'destroy' and vm is not None:
                vm.delete()


def controlVM(request):
    """Control operations on vm"""
    if request.method == "POST": 
        form = forms.controlVM(request.POST) 
        if form.is_valid(): 
            user_name = request.session['username']
            vm_uuid = form.cleaned_data['name'] 
            action = form.cleaned_data['action']

            ## we need to ensure that our UUIDs cannot collide
            try: 
                vm = models.VM.objects.get(uuid=vm_uuid)
            except: 
                vm = None 

            if action is 'power_on' and vm is not None:
                pass

            if action is 'power_off' and vm is not None:
                pass

            if action is 'vnc' and vm is not None:
                pass

    return HttpResponseRedirect('/clouds') 
