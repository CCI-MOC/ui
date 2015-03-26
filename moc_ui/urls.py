from django.conf.urls import patterns, include, url
from django.contrib import admin
from moc_ui.views import *

urlpatterns = patterns('',
    # front page
    url(r'^$', front_page),
    # user management 
#    url('^account', account),
    url(r'^login', login),
    url(r'^register', register),
    url(r'^logout', logout),
    # cloud splash
    url(r'^clouds', clouds),
    # projects control
    url(r'^createProject', createProject),
    url(r'^deleteProject', deleteProject),
    # projects control
    url(r'^createCluster', createCluster),
    url(r'^deleteCluster', deleteCluster),
    # vm control 
    url(r'^createVM', createVM),
    url(r'^deleteVM', deleteVM),
    url(r'^controlVM', controlVM),
#    # marketplace
#    url(r'^project_space/market', market),
#    # project settings
#    url(r'^project_space/manage/settings/deleteProject/(?P<projectName>.+)', deleteProject),
#    url(r'^project_space/manage/settings/addUser/(?P<projectName>.+)', addUser),
#    url(r'^project_space/manage/settings/editRole', editRole),
#    url(r'^project_space/manage/settings', settings),
#    # project management
#    url(r'^project_space/manage/delete/(?P<VMname>.+)', deleteVM),
#    url(r'^project_space/manage/create/(?P<VMname>.+);(?P<imageName>.+);(?P<flavorName>.+)', createVM),
#    url(r'^project_space/manage/create/(?P<VMname>.+)', createDefaultVM),
#    url(r'^project_space/manage/edit/controlVM', editControlVM),
#    url(r'^project_space/manage/edit', edit),
#    url(r'^project_space/manage', manage),
    # default
    url(r'^admin/', include(admin.site.urls)),
)
