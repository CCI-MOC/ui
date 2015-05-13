from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect

import models
import novaclient.v1_1.client as nvclient
import glanceclient.v2.client as glclient
import keystoneclient.v2_0.client as ksclient
import ui_api as api

class Login(forms.Form):
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegister(forms.ModelForm):
    user_name = forms.CharField(help_text="Please enter username.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter password.")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), )
    
    class Meta:
        model = models.User
        fields = ['user_name',]

    def save(self, force_insert=False, force_update=False, commit=True):
        new_user = super(UserRegister, self).save(commit=False)
        # Create new_user with 
        new_user = models.User(user_name=self.user_name)
        new_user.set_password(password=self.password)
        request.session['user_name'] = user_name

        if commit:
            new_user.save()
        return new_user 

# project actions
class UIProject(forms.ModelForm):
    # We need a custom init function to initialize the user from the request 
#    def __init__(self,request,*args,**kwargs):
#        # populates with request.POST 
#        super (UIProject,self ).__init__(*args,**kwargs)
#        print request.session["user_name"]
#        # populate user field with user_name
#        current_user = models.User.objects. \
#                                        filter(user_name=request.session["user_name"])
#        self.fields['users'].queryset = current_user
#        print "user being added to form is: %s" % current_user
#        for user in self.fields['users'].queryset:
#            print "part of query-set for 'users' is: %s" % user 

    class Meta:
        model = models.UIProject
        fields = ['name', ]
        # widgets = {'users': forms.HiddenInput()}

    def save(self, request, force_insert=False, force_update=False, commit=True):
        # Create new_user with 
        new_project = models.UIProject(name=self.cleaned_data['name'])
        if commit:
            new_project.save()
            new_project.users.add(request.session['user_name'])
            new_project.save()

        return new_project

# Cluster_Project actions
class ClusterProject(forms.ModelForm):

    class Meta:
        model = models.ClusterProject
        fields = ['name',]#'cluster', 'ui_project']

# vm actions

# class CreateVM(forms.Form):
#     name = forms.CharField()

#     def create(self):
# 	pass
    

# class DeleteVM(forms.Form):


class Create_VM(forms.Form):
    name = forms.CharField()
    cluster_projects = []
    for p in models.ClusterProject.objects.all().values('name').distinct(): #for all 
        cluster_projects.append((p['name'], p['name']))
    cluster_project = forms.ChoiceField(widget=forms.Select, choices=cluster_projects)

    #nova = api.get_nova(request, project)	#get nova object

    #image choices
    #image_choices = []
    #for option in nova.images.list():
    #    image_coices.append(str(option.name))    
    #imageName = forms.ChoiceField(widget=forms.Select, choices=image_choices)

    #flavor choices
    #flavor_choices = []
    #for option in nova.flavors.list():
    #    flavor_choices.append(str(option.name))
    #flavorName = forms.ChoiceField(widget=forms.Select, choices=flavor_choices)

class Delete_VM(forms.Form):

    name = forms.CharField()

class Control_VM(forms.Form):
    name = forms.CharField()
    action = forms.CharField()
