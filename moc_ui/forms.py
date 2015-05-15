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
        
# # project actions
# class CreateUIProject(forms.ModelForm):
#     def __init__(self,request,*args,**kwargs):
#         super (CreateUIProject, self).__init__(*args,**kwargs)

#     class Meta:
#         model = models.UIProject
#         fields = ['name', ]
#         # widgets = {'users': forms.HiddenInput()}

#     def save(self, request, force_insert=False, force_update=False, commit=True):
#         # Create new UIProject with user from request
#         new_ui_project = models.UIProject(name=self.cleaned_data['name'])
#         if commit:
#             new_ui_project.save()
#             # Add user as foreign key to UIProject
#             new_ui_project.users.add(request.session['user_name'])

#         return new_ui_project

# class DeleteUIProject(forms.ModelForm):
#     # Custom init function to initialize the correct projects 
#     def __init__(self,request,*args,**kwargs):
#         # populates function from the parent class with request.POST 
#         super (DeleteUIProject, self).__init__(*args,**kwargs)
#         # Grab current user object from request.session info
#         current_user = models.User.objects. \
#                                         get(user_name=request.session["user_name"])
#         # populate name field with projects owned by user 
#         project_names = models.UIProject.objects.filter(users=current_user)
#         self.fields['name'] = forms.ModelChoiceField(queryset=project_names)

#     class Meta:
#         model = models.UIProject
#         fields = ['name', ]

#     def save(self, force_insert=False, force_update=False, commit=True):
#         # Create new_user with 
#         new_ui_project = models.UIProject.objects.get(name=self.cleaned_data['name'])

#         print new_ui_project.name
#         print new_ui_project.id

#         if commit is True:
#             new_ui_project.delete()
#             return

#         return new_ui_project

# Cluster_Project actions
class ClusterProject(forms.ModelForm):

    class Meta:
        model = models.ClusterProject
        fields = ['name',]#'cluster', 'ui_project']

# # Cluster_Project actions
# class CreateClusterProject(forms.ModelForm):
#     def __init__(self,request,*args,**kwargs):
#         super (CreateClusterProject, self).__init__(*args,**kwargs)
#         # Grab current user object from request.session info
#         current_user = models.User.objects.get(user_name=request.session["user_name"])
#         # Populate ui_project field with projects owned by user 
#         ui_project_names = models.UIProject.objects.filter(users=current_user)
#         self.fields['ui_project'] = forms.ModelChoiceField(queryset=ui_project_names)
#         # Populate cluster field with clusters from db
#         clusters = models.Cluster.objects.all()
#         self.fields['cluster'] = forms.ModelChoiceField(queryset=clusters)

#     class Meta:
#         model = models.ClusterProject
#         fields = ['name', 'cluster', 'ui_project']

#     def save(self, request, force_insert=False, force_update=False, commit=True):
#         # Create new_user with 
#         new_cluster_project = models.ClusterProject(name=self.cleaned_data['name'],
#                                                     cluster=self.cleaned_data['cluster'],
#                                                     ui_project=self.cleaned_data['ui_project']
#                                                    )

#         if commit is True:
#             new_cluster_project.save()
#             return

#         return new_cluster_project

# class DeleteClusterProject(forms.ModelForm):
#     def __init__(self,request,*args,**kwargs):
#         # populates function from the parent class with request.POST 
#         super (DeleteClusterProject, self).__init__(*args,**kwargs)
#         # Grab current user object from request.session info
#         current_user = models.User.objects. \
#                                         get(user_name=request.session["user_name"])
#         # populate name field with Cluster projects owned by user 
#         cluster_project_list = models.ClusterProject.objects.filter(ui_project__users=current_user)
#         print cluster_project_list
#         print type(cluster_project_list)
#         self.fields['name'] = forms.ModelChoiceField(queryset=cluster_project_list)

#     class Meta:
#         model = models.ClusterProject
#         fields = ['name', ]

#     def save(self, force_insert=False, force_update=False, commit=True):
#         # Create new_user with 
#         new_cluster_project = models.ClusterProject.objects.get(name=self.cleaned_data['name'])

#         print new_cluster_project.name
#         print new_cluster_project.id

#         if commit is True:
#             new_cluster_project.delete()
#             return

#         return new_cluster_project

# vm actions
class Create_VM(forms.Form):

    # def __init__(self,request,*args,**kwargs):
    #     super (Create_VM, self).__init__(*args,**kwargs)

    # self.fields['name'] = forms.CharField()
    try:
        service = models.ClusterProject_service.objects.all().select_related('service')
    except Exception as e:
        print 'err'
        print e 

    name = forms.CharField()    


    # self.fields['image']  = forms.ChoiceField(widget =forms.Select, choices = ([(ubuntu,ubuntu),(centos,centos)]))
    # image =  forms.ChoiceField(widget =forms.Select, choices = ([(ubuntu,ubuntu),(centos,centos)]))
    image =  forms.ModelChoiceField(queryset = service, initial = 0)

        # flavor_list  = models.Service.objects.values('flavor')
        
        # medium = flavor_list[13]['flavor']
        # tiny = flavor_list[14]['flavor']

    m = 'm1.medium'
    t = 'm1.tiny'
    l = 'm1.large'
    s = 'm1.small'
    x = 'm1.xlarge'
    # self.fields['flavor'] = forms.ChoiceField(widget = forms.Select, choices = ([(m,m),(t,t),(l,l)]))
    flavor = forms.ChoiceField(widget = forms.Select, choices = ([(m,m),(x,x),(l,l),(s,s),(t,t)]))
    
  
    def save(self, request, force_insert=False, force_update=False, commit=True):
        
        name   = self.cleaned_data['name']
        image  = self.cleaned_data['image']
        flavor = self.cleaned_data['flavor']
        nova   = api.get_nova(request, 'ui') 

        api.createVM(nova, name, image, flavor)


        return 'here'

class Delete_VM(forms.Form):
    name = forms.CharField()

class Control_VM(forms.Form):
    name = forms.CharField()
    action = forms.CharField()




