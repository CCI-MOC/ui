from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import *

##Template Rendering and querying state
urlpatterns = patterns('',
    # front page
    url(r'^$', front_page),
    # cloud splash
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
#    # vm control 
#    url(r'^createVM', createVM),
#    url(r'^deleteVM', deleteVM),
#    url(r'^controlVM', controlVM),
)
