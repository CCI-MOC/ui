from django import forms

import models

class login(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class userRegister(forms.Form):
    username = forms.CharField(initial='Username')
    password = forms.CharField(initial='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(initial='Password', widget=forms.PasswordInput)

# project actions
class createProject(forms.Form):
    name = forms.CharField(initial='Project Name')

class deleteProject(forms.Form):
    name = forms.CharField(initial='Project Name')

# cluster actions
class createClusterAccount(forms.Form):
    clusters = [('buprod', 'BU-PROD'), ('huprod', 'HU-PROD'), ('neprod', 'NE-PROD'), 
                 ('umassprod', 'UMASS-PROD'), ('mitprod', 'MIT-PROD')]
    cluster = forms.ChoiceField(widget=forms.Select, choices=clusters)
    cluster_username = forms.CharField()
    cluster_password = forms.CharField(widget=forms.PasswordInput)

class deleteClusterAccount(forms.Form):
    cluster_username = forms.CharField(initial='Cluster Username')

# cluster Project actions
class createOSProject(forms.Form):
    clusterUsernames = []
    for p in models.ClusterAccount.objects.all().values('cluster_username').distinct():
        clusterUsernames.append((p['cluster_username'], p['cluster_username']))

    cluster = forms.ChoiceField(widget=forms.Select, choices=clusterUsernames)
    project_name = forms.CharField()
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class deleteOSProject(forms.Form):
    name = forms.CharField()

# vm actions
class createVM(forms.Form):
    name        = forms.CharField()

    osProjects = []
    for p in models.OSProject.objects.all().values('name').distinct():
        osProjects.append((p['name'], p['name']))

    OSProject = forms.ChoiceField(widget=forms.Select, choices=osProjects)

    projects    = []
    for p in models.UIProject.objects.all().values('name').distinct():
        projects.append((p['name'], p['name']))

    project     = forms.ChoiceField(widget=forms.Select, choices=projects)

class deleteVM(forms.Form):
    name = forms.CharField()

class controlVM(forms.Form):
    name = forms.CharField()
    action = forms.CharField()
