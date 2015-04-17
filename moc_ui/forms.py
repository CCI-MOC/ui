from django import forms
import models

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
        fields = ['name', 'cluster', 'ui_project']

# vm actions
class Create_VM(forms.Form):
    name = forms.CharField()

    cluster_projects = []
    for p in models.ClusterProject.objects.all().values('name').distinct():
        cluster_projects.append((p['name'], p['name']))

    cluster_project = forms.ChoiceField(widget=forms.Select, choices=cluster_projects)

class Delete_VM(forms.Form):
    name = forms.CharField()

class Control_VM(forms.Form):
    name = forms.CharField()
    action = forms.CharField()
