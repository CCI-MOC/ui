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


####################
## TEMPLATE VIEWS ##
####################

def front_page(request): 
    """ Front page; 
    
    Enter credentials to be processed by the login view 
    """ 
    
    return render(request, 'front_page.html', 
                 {'login_data': dicts.login_data, 'login_form': forms.Login(), 
                  'reg_modal': dicts.reg_modal, 'reg_form': forms.User_Register()}) 

def clouds(request): 
    """List projects and vms in user's clouds""" 
    
    createVMform = forms.Create_VM()

    user = helpers.Retrieve_Object("User", request.session['username'])

    try:
        projects = models.UI_Project.objects.filter(users=user)
    except Exception as e:
        print e 
        projects = []

    project_list = []
    for project in projects:
        vm_list = []
#        for vm in models.VM.objects.filter(ui_project=project):
#            vm_list.append(vm)
        project_list.append({'name':project.name, 'vm_list': vm_list})

    for project in dicts.test_project_list:
        project_list.append(project)


    return render(request, 'clouds.html', {'project_list': project_list, 'cloud_modals': dicts.cloud_modals, 'createVMform': createVMform })

def market(request, project):
    market_list = []
    # for market in markets:
    #     market_choice_list = []
    #     for choice in dicts.test_

    for market in dicts.test_market_list:
        market_list.append(market)

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
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']

            user = helpers.Retrieve_Object("User", user_name)
            if user is not None:
                if user.verify_password(password=password):
                    request.session['user_name'] = user_name
                    return HttpResponseRedirect('/clouds')

    return HttpResponseRedirect('/')

def logout(request):
    """View to Logout of session 

    remove session variables and return to login page 
    """
    for state, sessionInfo in request.session.items():
        sessionInfo = None

    return HttpResponseRedirect('/')
## STILL EXISTS BECAUSE OWEN IS WORKING ON LOGIN PAGE 
## I DON'T WANT TO RESTRUCTURE FORMS, WILL BE Create_Object
def register(request):
    """Register new user with keystone;

    called from login page Needs error checking 
    """

    if request.method == "POST":
        form = forms.User_Register(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']

            user = helpers.Retrieve_Object("User", user_name)
            if user is None:
                new_user = models.User(name=user_name)
                new_user.set_password(password=password)
                new_user.save()
                request.session['user_name'] = user_name
                return HttpResponseRedirect('/clouds')

    return HttpResponseRedirect('/')

## Default create view
def Create_Object(request, object_class):
    """Process POST form for generic Object 

    if the object doesn't exist and the user is registered,
    creates the object
    """
    if request.method == "POST":
        ## Concatinate object class to get correct form name
        form_name = "Create_%s" % object_class
        ## Grab class for db creation and initialize with POST info
        post_form = getattr(forms, form_name)(request.POST)
        if post_form.is_valid():
            ## Sort form variables into dicts of init variables and foreign keys
            init_dict = {}
            fk_dict = {}
            ## iterate through a sanatized dict of inputs
            for form_field, form_value in post_form.cleaned_data.iteritems():
                if '_fk' in form_field:
                    fk_dict.update({form_field:form_value})
                else:
                    init_dict.update({form_field:form_value})
            try:
                ## Grab Class for db creation
                initializer = getattr(models, object_class)
                ## Create new_object
                new_object = initializer(**init_dict)
            except Exception as e:
                print e 
                new_object = None

            ## Save object before adding many-to-many relation
            if new_object is not None:
                new_object.save()

            ## Iterate through foreign keys and add them to the 
            for fk in fk_dict:
                print blah

            user = helpers.Retrieve_Object("User", request.session['user_name'])

            try:
                new_object.users.add(user)
            except Exception as e:
                print e 
                new_object = None

            if new_object is not None:
                new_object.save()

    return HttpResponseRedirect('/clouds')

def Delete_Object(request, object_class):
    """Process form to delete an object.

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
                del_object.delete()

    return HttpResponseRedirect('/clouds')
