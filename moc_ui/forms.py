from django import forms

class login(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class userRegister(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

class dustProject(forms.Form):
    name = forms.CharField()
    action = forms.CharField()

class dustVM(forms.Form):
    name = forms.CharField()
    action = forms.CharField()

class controlVM(forms.Form):
    action = forms.CharField()
