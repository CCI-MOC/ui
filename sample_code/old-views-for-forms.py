from django.shortcuts import render
from django.http import HttpResponseRedirect
# Forms to use in pages
import forms
# Dictionaries to pass to template context
import dicts
# Models to access our db's tables
import models 
# Helper functions to make form processing easier 
import helpers 

### User Actions ###
def login(request):
    """ Login view; Checks post credentials, redirects
    to clouds or back to front page with error """
    if request.method == 'POST':
        form = forms.login(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']

            user = retrieveObject("User", user_name)
            if user is not None:
                if user.verify_password(password=password):
                    request.session['user_name'] = user_name
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
        form = forms.User_Register(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']

            user = retrieveObject("User", user_name)
            if user is None:
                new_user = models.User(name=user_name)
                new_user.set_password(password=password)
                new_user.save()
                request.session['user_name'] = user_name
                return HttpResponseRedirect('/clouds')

    return HttpResponseRedirect('/')

## Default create view
def Create_Object(request, object_class):
    """
    Process POST form for generic Object 
    if the object doesn't exist and the user is registered,
    creates the object
    """
    if request.method == "POST":
        ## concatinate object_class with create to get correct form
        form_name = "Create_%s" % object_class
        form = forms.form_name(request.POST)
        
        if form.is_valid():
            user = helpers.Retrieve_Object("User", request.session['user_name'])

            try:
                new_object = models.object_class(user=user, **form.cleaned_data)
            except:
                print "Error, %s not made" % object_class
                new_object = None

            if new_object is not None:
                new_object.save()

    return HttpResponseRedirect('/clouds')

def Delete_Object(request, object_class):
    """
    Process form to delete an object.
    if the object exists and user is registered,
    deletes object from database.
    """
    if request.method == "POST":
        ## grab the appropriate form
        form_name = "Create_%s" % object_class
        form = forms.form_name(request.POST)

        if form.is_valid():
            user = retrieve_object("User", request.session['user_name'])

            try:
                del_object = models.object_class.objects.get(user=user, **form.cleaned_data)
            except:
                print "Error, %s not made" % object_class
                del_object = None

            if del_object is not None:
                project.delete()

    return HttpResponseRedirect('/clouds')

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
            user = models.User.objects.get(name=request.session['user_name'])
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
            user = retrieveUser(request.session['user_name'])
            project_name = form.cleaned_data['name']

            try:
                project = models.UIProject.objects.get(name=project_name, user=user)
            except:
                project = None  

            if project is not None:
                project.delete()

    return HttpResponseRedirect('/clouds')

## cluster form processing
def createClusterAccount(request):
    """
    Process form to create a cluster, 
    if the cluster doesn't exist and user is registered,
    make new cluster in db
    """
    if request.method == "POST": 
        form = forms.createCluster(request.POST) 
        if form.is_valid(): 
            user = retrieveUser(request.session['user_name'])
            cluster_name = form.cleaned_data['cluster'] 
            cluster_user_name = form.cleaned_data['cluster_user_name'] 
            cluster_password = form.cleaned_data['cluster_password'] 

            try:
                cluster = models.Cluster.objects.get(name=cluster_name, user=user) 
            except:
                try:
                    cluster = models.Cluster(title=cluster_name, auth_url="http://140.247.152.207" )
                    cluster.save()
                except:
                    print "Couldn't create cluster"
                    return HttpResponseRedirect('/')


            if cluster is not None and user is not None:
                try:
                    clusterAccount = models.ClusterAccount(cluster_user_name=cluster_user_name, cluster_password=cluster_password, 
                                             cluster=cluster, user=user) 
                except:
                    clusterAccount = None

                if clusterAccount is not None:
                    clusterAccount.save()

    return HttpResponseRedirect('/clouds')

def deleteClusterAccount(request):
    if request.method == "POST": 
        form = forms.deleteCluster(request.POST)
        if form.is_valid():
            user = retrieveUser(request.session['user_name'])
            osProject_name = form.cleaned_data['name'] 

            try:
                OSProject = models.OSProject.objects.get(name=osProject_name, user=user) 
            except: 
                OSProject = None 

            if cluster is not None:
                cluster.delete()

    return HttpResponseRedirect('/clouds') 

def createOSProject(request):
    if request.method == "POST":
        form = forms.createOSProject(request.POST) 
    
def deleteOSProject(request):
    if request.method == "POST":
        form = forms.createOSProject(request.POST) 

## vm form processing
def createVM(request):
    """Process form to create vm"""
    if request.method == "POST":
        form = forms.createVM(request.POST)
        if form.is_valid():
            user = retrieveUser(request.session['user_name'])
            vm_name = form.cleaned_data['name']
            OSProject = form.cleaned_data['provider']
            try: 
                vm = models.VM.objects.get(name=vm_name)
            except:
                vm = None

            if vm is None:
                vm = models.VM(name=vm_name)
                vm.save()
    return HttpResponseRedirect('/clouds')

def deleteVM(request):
    """Process form to delete vm"""
    if request.method == "POST":
        form = forms.deleteVM(request.POST)
        if form.is_valid():
            user = retrieveUser(request.session['user_name'])
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
            user_name = request.session['user_name']
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
