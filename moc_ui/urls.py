from django.conf.urls import patterns, include, url
from django.contrib import admin
from marketUI.views import *

urlpatterns = patterns('',
    # login 
    url(r'^login/register', register),
    url(r'^logout/', logout),
    url(r'^login/', login),
    # projects
    url(r'^projects/enterProject', enterProject),
    url(r'^projects/create', createProject),
    url(r'^projects/', projects),
    # marketplace
    url(r'^project_space/market', market),
    # project settings
    url(r'^project_space/manage/settings/deleteProject/(?P<projectName>.+)', deleteProject),
    url(r'^project_space/manage/settings/addUser/(?P<projectName>.+)', addUser),
    url(r'^project_space/manage/settings/editRole', editRole),
    url(r'^project_space/manage/settings', settings),
    # project management
    url(r'^project_space/manage/delete/(?P<VMname>.+)', deleteVM),
    url(r'^project_space/manage/create/(?P<VMname>.+);(?P<imageName>.+);(?P<flavorName>.+)', createVM),
    url(r'^project_space/manage/create/(?P<VMname>.+)', createDefaultVM),
    url(r'^project_space/manage/edit/controlVM', editControlVM),
    url(r'^project_space/manage/edit', edit),
    url(r'^project_space/manage', manage),
    # default
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login)
)
