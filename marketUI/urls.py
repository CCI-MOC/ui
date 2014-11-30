from django.conf.urls import patterns, include, url
from django.contrib import admin
from marketUI.views import *

urlpatterns = patterns('',
    
    url(r'^login/create_user', create_user),
    url(r'^login/', login),
    url(r'^projects/', projects),

    url(r'^project_space/market', market),
    url(r'^project_space/manage/settings', settings),
    url(r'^project_space/manage/delete/(?P<VMname>.+)', deleteVM),
    url(r'^project_space/manage/create/(?P<VMname>.+);(?P<imageName>.+);(?P<flavorName>.+)', createVM),
    url(r'^project_space/manage/create/(?P<VMname>.+)', createDefaultVM),
    url(r'^project_space/manage', manage),

    # EXAMPLE REGEX
    # url(r'^races/(?P<session_id>\d+)$', 'races', name='races'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login)
)
