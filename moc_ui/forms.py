from django import forms

class login(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class userRegister(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

class createProject(forms.Form):
    name = forms.CharField()
    action = forms.CharField(widget=forms.HiddenInput(), initial='create')

class deleteProject(forms.Form):
    name = forms.CharField()
    action = forms.CharField(widget=forms.HiddenInput(), initial='delete')

class createVM(forms.Form):
    providers = ['BU-PROD', 'HU-PROD', 'NE-PROD', 'UMASS-PROD', 'MIT-PROD']
    name = forms.CharField()
    provider= forms.ChoiceField(widget=forms.RadioSelect, choices=providers)
    action = forms.CharField(widget=forms.HiddenInput(), initial='create')

class deleteVM(forms.Form):
    name = forms.CharField()
    action = forms.CharField(widget=forms.HiddenInput(), initial='delete')

class controlVM(forms.Form):
    action = forms.CharField()
