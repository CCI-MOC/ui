from django import forms

import models

class Login(forms.Form):
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class User_Register(forms.Form):
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

# project actions
class Create_UI_Project(forms.Form):
    name = forms.CharField(initial='Project Name')


class Delete_UI_Project(forms.Form):
    name = forms.CharField(initial='Project Name')

# cluster actions
class Create_Cluster_Account(forms.Form):
    clusters = [('Boston University', 'BU-PROD'), 
                ('Harvard University', 'HU-PROD'), 
                ('North Eastern University', 'NE-PROD'), 
                ('University of Massachusettes', 'UMASS-PROD'), 
                ('Massachusettes Institute of Technology', 'MIT-PROD')]

    cluster = forms.ChoiceField(widget=forms.Select, choices=clusters)
    cluster_user_name = forms.CharField()
    cluster_tenant = forms.CharField()
    cluster_password = forms.CharField(widget=forms.PasswordInput)

class Delete_Cluster_Account(forms.Form):
    cluster_user_name = forms.CharField(initial='Cluster Username')

# Cluster_Project actions
class Create_Cluster_Project(forms.Form):
    cluster_user_names = []
    for account in models.Cluster_Account.objects.all().values('cluster_user_name').distinct():
        cluster_user_names.append((account['cluster_user_name'], account['cluster_user_name']))

    cluster_user_name = forms.ChoiceField(widget=forms.Select, choices=cluster_user_names)
    project_name = forms.CharField()
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class Delete_Cluster_Project(forms.Form):
    name = forms.CharField()

# vm actions
class Create_VM(forms.Form):
    name = forms.CharField()

    cluster_projects = []
    for p in models.Cluster_Project.objects.all().values('name').distinct():
        cluster_projects.append((p['name'], p['name']))

    cluster_project = forms.ChoiceField(widget=forms.Select, choices=cluster_projects)

    projects    = []
    for p in models.UI_Project.objects.all().values('name').distinct():
        projects.append((p['name'], p['name']))

    project     = forms.ChoiceField(widget=forms.Select, choices=projects)

class Delete_VM(forms.Form):
    name = forms.CharField()

class Control_VM(forms.Form):
    name = forms.CharField()
    action = forms.CharField()
