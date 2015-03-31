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
                    {'id': 'createClusterAccount', 'action': '/createClusterAccount', 'title': 'Add Cluster Account', 'form': forms.createClusterAccount()},
                    {'id': 'deleteClusterAccount', 'action': '/deleteClusterAccount', 'title': 'Delete Openstack Project', 'form': forms.deleteClusterAccount()},
                    {'id': 'createOSProject', 'action': '/createOSProject', 'title': 'Add Cluster Project', 'form': forms.createOSProject()},
                    {'id': 'deleteOSProject', 'action': '/deleteOSProject', 'title': 'Delete Cluster Project', 'form': forms.deleteOSProject()},
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
            vm_list.append(vm)
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

