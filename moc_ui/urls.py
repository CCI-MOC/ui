from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import *

##Template Rendering and querying state
urlpatterns = patterns('',
    # front page
    url(r'^$', front_page),
    # cloud splash
<<<<<<< HEAD
    url(r'^clouds', clouds),
    # about page
    url(r'^about', about),
    # terms page
    url(r'^terms',terms),
    # help page
    url(r'^help', helps),
    # marketplace
    url(r'^(?!.+toggle_active\/?$|.+toggle_default\/?$)market\/(?P<project>.+)?\/$', market),
    # Market Place filtering functionality:
    #url(r'^market\/(?P<project>.+)\/(?P<filter>.+)\/?$', market),
    url(r'^(?!.+toggle_active\/?$|.+toggle_default\/?$)market\/(?P<project>.+)?\/(?P<filter>.+)\/?$', market),

    # Tells the view to perform an action on a service. 
    url(r'^market\/(?P<project>.+)\/(?P<service>.+)\/(?P<action>toggle_active|toggle_default)\/?$', market),
=======
    url(r'^projects', projects),
    # market page
    url(r'^(?!.+toggle_active\/?$|.+toggle_default\/?$)market\/(?P<project>.+)?\/$', market),
    # Market Place filtering functionality:
    url(r'^(?!.+toggle_active\/?$|.+toggle_default\/?$)market\/(?P<project>.+)?\/(?P<filter>.+)\/?$', market),
    # Tells the view to perform an action on a service. 
    url(r'^market\/(?P<project>.+)\/(?P<service>.+)\/(?P<action>toggle_active|toggle_default)\/?$', market),
    # project control page
    url(r'^control\/(?P<project>.+)?\/$', control),
    #
    url(r'^network\/(?P<project>.+)?\/$', network),
	#VM pause/unpause
    url(r'^VM_active_state_toggle\/(?P<project>.+)?\/(?P<VMid>.+)\/?$', VM_active_state_toggle),
    #VM default add
    url(r'VM_add_default\/(?P<project>.+)\/?$', VM_add_default),
    #VM add
    #url(r'VM_add\/(?P<project>.+)?\/(?P<VMname>.+)?\/(?P<imageName>.+)?\/(?P<flavorName>.+)\/?$',  VM_add),
    #VM delete
    url(r'VM_delete\/(?P<project>.+)?\/(?P<VMid>.+)\/?$', VM_delete),
    #VM start
    url(r'VM_start\/(?P<project>.+)?\/(?P<VMid>.+)\/?$', VM_start),

    #VM stop
    url(r'VM_stop\/(?P<project>.+)?\/(?P<VMid>.+)\/?$', VM_stop)
>>>>>>> lucasRefactor
)
##Form Processing
urlpatterns += patterns('',
    # user management 
    url(r'^login', login),
    url(r'^register', register),
    url(r'^logout', logout),
    ## DB dusting
    url(r'^create/(?P<object_class>.+)', create_object),
    url(r'^delete/(?P<object_class>.+)', delete_object),
    # VM creatoin
    url(r'^VM_add', VM_add),
    # projects control
#    url(r'^createProject', createProject),
#    url(r'^deleteProject', deleteProject),
#    # cluster control
#    url(r'^createClusterAccount', createClusterAccount),
#    url(r'^deleteClusterAccount', deleteClusterAccount),
#    url(r'^createOSProject', createOSProject),
#    url(r'^deleteOSProject', deleteOSProject),
#    # vm control 
#    url(r'^createVM', createVM),
#    url(r'^deleteVM', deleteVM),
#    url(r'^controlVM', controlVM),
)
