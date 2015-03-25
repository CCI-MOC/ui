from django.shortcuts import render
from django.http import HttpResponseRedirect
# Forms to use in pages
import forms
# Dictionaries to pass to template context
import dicts
# Models to access our db's tables
import models 

### Template Pages ### 
def front_page(request): 
    """ Front page; Enter credentials to be processed by the login view """ 
    
    return render(request, 'front_page.html', 
                 {'login_data': dicts.login_data, 'login_form': forms.login(), 
                  'reg_modal': dicts.reg_modal, 'reg_form': forms.userRegister()}) 

def clouds(request): 
    """List projects and vms in user's clouds""" 
    
    cloud_modals = [{'id': 'createProject', 'title': 'Create Project', 'form': forms.createProject()},
                    {'id': 'deleteProject', 'title': 'Delete Project', 'form': forms.deleteProject()},
                    {'id': 'createCluster', 'title': 'Create Cluster', 'form': forms.createCluster()},
                    {'id': 'deleteCluster', 'title': 'Delete Cluster', 'form': forms.deleteCluster()},
                    {'id': 'createVM', 'title': 'Create VM', 'form': forms.createVM()},
                    {'id': 'deleteVM', 'title': 'Delete VM', 'form': forms.deleteVM()},]

    try:
        user = models.User.objects.get(name=request.session['username'])
        projects = models.UIProject.objects.filter(user=user)
    except:
        pass

    project_list = []
    for project in projects:
        vm_list = []
        for vm in models.VM.objects.filter(project=project):
            vm_list.append(vm.name)
        project_list.append({'name':project.name, 'vm_list': vm_list})

    for project in dicts.test_project_list:
        project_list.append(project)


    return render(request, 'clouds.html', {'project_list': project_list, 'cloud_modals': cloud_modals})

### User Actions ###
def login(request):
    """ Login view; Checks post credentials, redirects
    to clouds or back to front page with error """
    if request.method == 'POST':
        form = forms.login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = models.User.objects.get(name=username)
                if user.verify_password(password=password):
                    request.session['username'] = username
                    return HttpResponseRedirect('/clouds')
            except:
                pass
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

            try:
                user = models.User.objects.get(name=username)
            except models.User.DoesNotExist:
                user = None

            if user is None:
                newuser = models.User(name=username)
                newuser.set_password(password=password)
                newuser.save()
                request.session['username'] = username
                return HttpResponseRedirect('/clouds')

    return HttpResponseRedirect('/')

def dustProject(request):
    """Create or destroy project - from dust to dust"""
    if request.method == "POST":

        form = forms.createProject(request.POST)
        if form.is_valid():
            user = models.User.objects.get(name=request.session['username'])
            project_name = form.cleaned_data['name']
            action = form.cleaned_data['action']

            if action == 'create':
                project = models.Project(name=project_name, user=user)
                project.save()
                return HttpResponseRedirect('/clouds')

        form = forms.deleteProject(request.POST)
        if form.is_valid():
            try:
                project = models.Project.objects.get(name=project_name, user=user)
                if action == 'destroy' and 'pk' in project:
                    project.delete()
            except:
                pass

    return HttpResponseRedirect('/clouds')

def dustCluster(request):
    """Create or destroy cluster - from dust to dust"""
    if request.method == "POST": 
        try:
            user = models.User.objects.get(name=request.session['username'])
        except:
            print "No such user"
            return HttpResponseRedirect('/') 

        form = forms.createCluster(request.POST) 
        if form.is_valid(): 
            cluster_name = form.cleaned_data['name'] 
            cluster_user_name = form.cleaned_data['user_name'] 
            cluster_password = form.cleaned_data['password'] 
            endpoint = form.cleaned_data['endpoint'] 

            if action == 'create':
                cluster = models.Cluster(name=cluster_name, user_name=cluster_user_name, password=cluster_password, 
                                         endpoint=endpoint, user=user) 
                cluster.save()
                return HttpResponseRedirect('/clouds')

        form = forms.deleteCluster(request.POST)
        if form.is_valid():
            cluster_name = form.cleaned_data['name'] 
            action = form.cleaned_data['action']

            try:
                cluster = models.Cluster.objects.get(name=cluster_name, user=user) 
            except: 
                cluster = None 

            if action == 'destroy' and cluster is not None:
                cluster.delete()

    return HttpResponseRedirect('/clouds') 
    
def dustVM(request):
    """Create or destroy vm - from dust to dust"""
    if request.method == "POST":
        try:
            user = models.User.objects.get(name=request.session['username'])
        except:
            print "No such user"
            return HttpResponseRedirect('/') 

        form = forms.createVM(request.POST)
        if form.is_valid():
            vm_name = form.cleaned_data['name']
            OSProject = form.cleaned_data['cloud']
            try: 
                vm = models.VM.objects.get(name=vm_name, user=user)
            except:
                vm = None

            if action == 'create' and vm is None:
                vm = models.VM(name=vm_name, user=user)
                vm.save()
                return HttpResponseRedirect('/clouds')

        form = forms.deleteVM(request.POST)
        if form.is_valid():
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
