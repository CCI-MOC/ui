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


def clouds(request): 
    """List projects and vms in user's clouds""" 
    

    user = helpers.retrieve_object("User", "user_name", request.session['user_name'])
    if user is not None:
        try:
            projects = models.UIProject.objects.filter(users=user)
            #print projects
        except Exception as e:
            print e 
            projects = []
    else:
        return HttpResponseRedirect('/')


    project_list = []
    for project in projects:
        vm_list = []
#        for vm in models.VM.objects.filter(ui_project=project):
#            vm_list.append(vm)
        project_list.append({'name':project.name, 'vm_list': vm_list})

    for project in dicts.test_project_list:
        project_list.append(project)


    return render(request, 'clouds.html', 
                  {'project_list': project_list, 
                   'cloud_modals': html.cloud_modals(request), 
                  }
                 )

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
    to clouds or back to front page with error 
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
                    return HttpResponseRedirect('/clouds')

    # temporary workaround to auto-login
    print "using workaround"
    request.session['user_name'] = "jbell" 
    return HttpResponseRedirect('/clouds')

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
                return HttpResponseRedirect('/clouds')
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
        form_name = "Create%s" % object_class
        # Passing request.POST for django auto-pop, request to pull session info out
        post_form = getattr(forms, form_name)(request, request.POST)
        # Debug code to print form html to console
        #for field in post_form:
           #print "%s: %s" % (field.label_tag(), field.value())
        if post_form.is_valid():
            # Debug code to print form info in better format
            #for key, value in post_form.cleaned_data.iteritems():
                #print "%s: %s" % (key, value)
            try:
                # Call the save function on the form 
                new_object = post_form.save(request)
            except Exception as e:
                print "Hit exception:"
                print e 
        else:
            print post_form.errors
    return HttpResponseRedirect('/clouds')

def delete_object(request, object_class):
    """Process POST form to delete generic database object"""
    if request.method == "POST":
        form_name = "Delete%s" % object_class
        # Grab form class and initialize with request and POST info
        post_form = getattr(forms, form_name)(request, request.POST)
        # Debug code to print form html to console
#        for field in post_form:
#            print "%s: %s" % (field.label_tag(), field.value())
        if post_form.is_valid():
            # Debug code to print form info in better format
#            for key, value in post_form.cleaned_data.iteritems():
#                print "%s: %s" % (key, value)
#            print "end of form data"
            try:
                # Call the save function on the form 
                form_object = post_form.save()
                #print "name: %s" % form_object
                #print "id: %d" % form_object.id
            except Exception as e:
                print "Hit exception:"
                print e 
        else:
            print post_form.errors
    return HttpResponseRedirect('/clouds')

def control_vm(request, action, vm_name):
    if request.method == "PUT":
    # check that the user has privalidge on vm
    # actually do the action
        pass
