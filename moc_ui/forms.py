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
    action = forms.CharField(widget=forms.HiddenInput(), initial='create')

class deleteProject(forms.Form):
    name = forms.CharField()
    action = forms.CharField(widget=forms.HiddenInput(), initial='delete')

# cluster actions
class createCluster(forms.Form):
    OpenStackUsername = forms.CharField()
    OpenStackPassword = forms.CharField(widget=forms.PasswordInput)
    OpenStackEndpoint = forms.URLField()

class deleteCluster(forms.Form):
    OpenStackUsername = forms.CharField()
    OpenStackPassword = forms.CharField(widget=forms.PasswordInput)
    OpenStackEndpoint = forms.URLField()

# vm actions
class createVM(forms.Form):
    providers = [('buprod', 'BU-PROD'), ('huprod', 'HU-PROD'), ('neprod', 'NE-PROD'), 
                 ('umassprod', 'UMASS-PROD'), ('mitprod', 'MIT-PROD')]
    name = forms.CharField()
    provider= forms.ChoiceField(widget=forms.RadioSelect, choices=providers)
    action = forms.CharField(widget=forms.HiddenInput(), initial='create')

class deleteVM(forms.Form):
    name = forms.CharField()
    action = forms.CharField(widget=forms.HiddenInput(), initial='delete')

class controlVM(forms.Form):
    action = forms.CharField()
