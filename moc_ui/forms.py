from django import forms

class login(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class userRegister(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

# project actions
class createProject(forms.Form):
    name = forms.CharField()

class deleteProject(forms.Form):
    name = forms.CharField()

# cluster actions
class createCluster(forms.Form):
    name = forms.CharField()
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    endpoint = forms.URLField()

class deleteCluster(forms.Form):
    name = forms.CharField()

# vm actions
class createVM(forms.Form):
    providers = [('buprod', 'BU-PROD'), ('huprod', 'HU-PROD'), ('neprod', 'NE-PROD'), 
                 ('umassprod', 'UMASS-PROD'), ('mitprod', 'MIT-PROD')]
    name = forms.CharField()
    provider= forms.ChoiceField(widget=forms.Select, choices=providers)

class deleteVM(forms.Form):
    name = forms.CharField()

class controlVM(forms.Form):
    name = forms.CharField()
    action = forms.CharField()
