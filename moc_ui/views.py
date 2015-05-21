# Django helpers for rendering html and redirecting
from django.shortcuts import render
from django.http import HttpResponseRedirect
# Dictionaries to pass to template context
import dicts
# Forms to use in pages
import forms
# Models to access our database's tables
import models 
# Helper functions to make form processing easier 
import query_helpers as helpers
# HTML descriptions mixed with modal calls, 
# passed to template context in order to
# render modal / button / table templates
import html_helpers as html


from models import Service, ClusterProject

from models import UIProject

#API for keystone, nova and other services 
import ui_api as api


####################
## TEMPLATE VIEWS ##
####################

def front_page(request): 
    """ Front page; 
    
    Enter credentials to be processed by the login view 
    """ 

    return render(request, 'front_page.html', 
                 {'login_data': dicts.login_data, 'login_form': forms.Login(), 
                  'reg_modal': dicts.reg_modal, 'reg_form': forms.UserRegister()}) 


def about(request):
    return render(request,"aboutPage.html")

def terms(request):
    return render(request, "termsPage.html")

def helps(request):
    return render(request, 'helpPage.html')



def projects(request):

    tenant = api.joinTenant(request, 'ui')
    project_name =  models.ClusterProject.objects.all()
    project_list = []
    for project in project_name:
        project_list += [{'name': project}]
    return render(request, 'projects.html', 
                  {'project_list': project_list, 
                   'project_modals': html.project_modals(request)
                   })
  
## Project Control Page
def control(request, project):
  
    vms = api.listVMs(api.get_nova(request, project))

    return render(request, 'control.html', 
                  {'project': [project], 'vms': vms,
                   'vm_modals': html.vm_modals(request)
                    })
## Network Page
def network(request, project):
    

    return render(request, 'network.html',
                    {'project': [project]})

## Network Page
def storage(request, project):
    

    return render(request, 'storage.html',
                    {'project': [project]})




#def login(request):
#    """View to Login a user
#   
#    Checks post credentials, redirects
#    to projects or back to front page with error 
#    """
#    if request.method == 'POST':
#        form = forms.Login(request.POST)
#        if form.is_valid():
#            print "form is valid"
#            user_name = form.cleaned_data['user_name']
#            password = form.cleaned_data['password']
#
#            user = helpers.retrieve_object("User", "user_name", user_name)
#            if user is not None:
#                print "verifying password"
#                if user.verify_password(password=password):
#                    request.session['user_name'] = user_name
#                    request.session['username'] = user_name
#                    request.session['password'] = password
#                    return HttpResponseRedirect('/projects')




## Market Page
def market(request, project, filter = 'all', service = '', action = ''):
    def _toggle_active (project, service):
        #Get the models of the queried objects:
        project = UIProject.objects.filter(name = project)
        service = Service.objects.filter(name = service)

        # Fails if a project or service does not exist, return an error. 
        if len(project) == 0 or len(service) == 0:
            return False

        # Checks if the relation already exist
        search = models.UIProject_service_list.objects.filter(project = project, service = service)
        if len(search) > 0:
            search[0].delete()
        else:
            uipr_serv = models.UIProject_service_list (service = service[0], project = project[0], type = 'NOR')
            uipr_serv.save()
        return True

    def toggle_active (project, service):
        #Get the models of the queried objects:
        project = ClusterProject.objects.filter(name = project)
        service = Service.objects.filter(name = service)

        # Fails if a project or service does not exist, return an error. 
        if len(project) == 0 or len(service) == 0:
            return False

        # Checks if the relation already exist
        search = models.ClusterProject_service.objects.filter(project = project, service = service)
        if len(search) > 0:
            search[0].delete()
        else:
            uipr_serv = models.ClusterProject_service (service = service[0], project = project[0], default = False)
            uipr_serv.save()
        return True

    def _toggle_default (project, service):
        #Get the models of the queried objects:
        project = UIProject.objects.filter(name = project)
        service = Service.objects.filter(name = service)

        # Fails if a project or service does not exist, return an error. 
        if len(project) == 0 or len(service) == 0:
            return False

        # Checks if the relation already exist
        # Toggles the state of the relationship
        search = models.UIProject_service_list.objects.filter(project = project, service = service)
        if len(search) > 0:
            if search[0].type == 'NOR':
                search[0].type = 'DEA'
            else:
                search[0].type = 'NOR'
            search[0].save()
        else:
            uipr_serv = models.UIProject_service_list (service = service[0], project = project[0], type = 'DEA')
            uipr_serv.save()
        return True

    def toggle_default (project, service):
        #Get the models of the queried objects:
        project = ClusterProject.objects.filter(name = project)
        service = Service.objects.filter(name = service)

        # Fails if a project or service does not exist, return an error. 
        if len(project) == 0 or len(service) == 0:
            return False

        # Checks if the relation already exist
        # Toggles the state of the relationship
        search = models.ClusterProject_service.objects.filter(project = project, service = service)
        search2 = models.ClusterProject_service.objects.filter(project = project)
        
        for r in search2:
            if r.service.service_type == service[0].service_type and r.service.name != service[0].name:
               
                r.default = False
                r.save()
        if len(search) > 0:
            if not search[0].default:
                search[0].default = True
            else:
                search[0].default = False
            search[0].save()
        else:
            uipr_serv = models.ClusterProject_service (service = service[0], project = project[0], default = True)
            uipr_serv.save()
        return True

    def _check_status (service, project = project):
        #Get the models of the queried objects:
        project = UIProject.objects.filter(name = project)
        service = Service.objects.filter(name = service)
        
        # Fails if a project or service does not exist, return an error. 
        if len(project) == 0 or len(service) == 0:
            return (False, False, 'Failure')

        search = models.UIProject_service_list.objects.filter(project = project, service = service)
        if len(search) == 0:
            return (False, False)
        elif len(search) > 0 and search[0].type == 'NOR':
            return (True, False)
        else:
            return (True, True)

    def check_status (service, project = project):
        #Get the models of the queried objects:
        project = ClusterProject.objects.filter(name = project)
        service = Service.objects.filter(name = service)
        
        # Fails if a project or service does not exist, return an error. 
        if len(project) == 0 or len(service) == 0:
            return (False, False, 'Failure')

        search = models.ClusterProject_service.objects.filter(project = project, service = service)
        if len(search) == 0:
            return (False, False)
        elif len(search) > 0 and not search[0].default:
            return (True, False)
        else:
            return (True, True)

    if service != '' and action != '':
        print('hit')
        if action == 'toggle_active':
            if toggle_active (project, service):
                print('t_a_s')
        else:
            if toggle_default (project, service):
                print ('t_d_s')
       
        return HttpResponseRedirect('/market/' + project + '/')
    market_list = [x.__dict__ for x in Service.objects.all() if x.service_type == filter or filter == 'all']
    for x in market_list:
        cs = check_status(x['name'], project)
        x['act'] = cs[0]
        x['dea'] = cs[1]

    return render(request, 'market.html', {'project': project, 'market_list': market_list})

################
## FORM VIEWS ##
################

### User Actions ###
def login(request):
    """View to Login a user
    
    Checks post credentials, redirects
    to projects or back to front page with error 
    """
    if request.method == 'POST':
        form = forms.Login(request.POST)
        if form.is_valid():
            print "form is valid"
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']

            user = helpers.retrieve_object("User", "user_name", user_name)
            if user is not None:
                print "verifying password"
                if user.verify_password(password=password):
                    request.session['user_name'] = user_name
                    request.session['username'] = user_name
                    request.session['password'] = password
                    return HttpResponseRedirect('/projects')

def logout(request):
    """View to Logout of session 

    remove session variables and return to login page 
    """
    for state, sessionInfo in request.session.items():
        sessionInfo = None

    return HttpResponseRedirect('/')
## STILL EXISTS BECAUSE OWEN IS WORKING ON LOGIN PAGE 
## I DON'T WANT TO RESTRUCTURE REG FORMS, WILL BE Create_Object
def register(request):
    """Register new user with keystone;

    called from login page Needs error checking 
    """

    if request.method == "POST":
        form = forms.UserRegister(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']

            user = helpers.retrieve_object("User", "user_name", user_name)
            if user is None:
                new_user = models.User.create_user(user_name=user_name,
                                                   password=password)
                new_user.save()
                request.session['user_name'] = user_name
                request.session['username'] = user_name
                request.session['password'] = password
                return HttpResponseRedirect('/projects')
            else:
                print "user %s exists" % user
        else:
            print form.errors 
        

    return HttpResponseRedirect('/')

# Generic dust views
# Earth to earth, ashes to ashes, dust to dust
def create_object(request, object_class):
    """Process POST form to create generic database object"""
    if request.method == "POST":
        # get the current user for auth and fk creation
        current_user = request.session['user_name']
        # Grab form class for object creation and initialize with request info
        # Passing request.POST for django auto-pop, request to pull session info out
        post_form = getattr(forms, object_class)(request.POST)
        # Debug code to print form html to console
        for field in post_form:
           print "%s: %s" % (field.label_tag(), field.value())
        if post_form.is_valid():
            # Debug code to print form info in better format
            for key, value in post_form.cleaned_data.iteritems():
                print "%s: %s" % (key, value)
            try:
                # Creates a new database object
                # Saves the new object by default
                new_object = post_form.save(request)
                # Create the foreing key and many-to-many relations
                #new_object.users.add(current_user)
                #new_object.save()
                # iterate through fks and print them out
                object_model = getattr(models, object_class)
                print "object model: %s" % object_model
                print "fields: "
                field_names = []
                for field in object_model._meta.get_fields():
                    print field
                    field_names.push(field_names)
#                for field, field_name in object_model._meta.fields:
#                    print field_name 
#                    if field.many_to_many:
#                        print field.rel.to
            except Exception as e:
                print "Hit exception:"
                print e 
        else:
            print post_form.errors
    return HttpResponseRedirect('/projects')

def delete_object(request, object_class):
    """Process POST form to delete generic database object"""
    if request.method == "POST":
        # Grab form class for object deletion and initialize with request and POST info
        post_form = getattr(forms, object_class)(request.POST, request)
        # Debug code to print form html to console
        for field in post_form:
            print "%s: %s" % (field.label_tag(), field.value())
        if post_form.is_valid():
            # Debug code to print form info in better format
            for key, value in post_form.cleaned_data.iteritems():
                print "%s: %s" % (key, value)
            try:
                # Create a database object from the post form, but doesn't commit
                form_object_from_form = post_form.save(commit=False)
                # Delete object, commits to database
                form_object_from_form.delete()
            except Exception as e:
                print "Hit exception:"
                print e 
        else:
            print post_form.errors
    return HttpResponseRedirect('/projects')

def control_vm(request, action, vm_name):
    if request.method == "PUT":
    # check that the user has privalidge on vm
    # actually do the action
        pass

# VM CONTROLS
def VM_active_state_toggle (request, project, VMid):
    print  (project, VMid)
    print  VMid[len(VMid)-1]
    print  VMid[:len(VMid)-1]
    if VMid[len(VMid)-1] == '/':
        VMid = VMid[:len(VMid)-1]
    nova = api.get_nova(request, project)
    api.VM_active_state_toggle(nova, VMid)
    return HttpResponseRedirect('/control/' + project + '/')

# VM Delete
def VM_delete(request, project, VMid):
    print (project, VMid)                   #debugging
    if VMid[len(VMid)-1] == '/':            #strip ending /
        VMid = VMid[:len(VMid)-1]
    nova = api.get_nova(request, project)   #get nova object
    api.delete(nova, VMid)                  #delete specified Nova object
    return HttpResponseRedirect('/control/' + project + '/')    #back to control

# VM start
def VM_start(request, project, VMid):
    print (project, VMid)                   #debugging
    if VMid[len(VMid)-1] == '/':            #strip ending /
        VMid = VMid[:len(VMid)-1]
    nova = api.get_nova(request, project)   #get nova object
    api.startVM(nova, VMid)                 #start specified Nova object
    return HttpResponseRedirect('/control/' + project + '/')    #back to control

# VM stop
def VM_stop(request, project, VMid):
    print (project, VMid)                   #debugging
    if VMid[len(VMid)-1] == '/':            #strip ending /
        VMid = VMid[:len(VMid)-1]
    nova = api.get_nova(request, project)   #get nova object
    api.stopVM(nova, VMid)                  #stop specified Nova object
    return HttpResponseRedirect('/control/' + project + '/')    #back to control

# VM add default
def VM_add_default(request, project):
    print (project)
    nova = api.get_nova(request, project)   #get nova object
    api.createDefault(nova)
    return HttpResponseRedirect('/control/' + project + '/')    #back to control

# VM add custom
def create_VM(request, project):
    print 'lucas-test-enter-view-create_VM'
    if request.method == 'POST':
        form = forms.Create_VM(request.POST)
        
        if form.is_valid():
            print 'lucas-test-view-create_VM_beforeSave'
            try:
                form.save(request)
            except Exception as e:
                print "Hit exception:"
                print e 

            print 'lucas-test-view-create_VM_afterSave'
        else:
            for field in form:
                print "%s: %s" % (field.label_tag(), field.value()) 

            print form.errors

    return HttpResponseRedirect('/control/' + project + '/')    