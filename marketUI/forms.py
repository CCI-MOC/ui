from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class TenantLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    tenantName = forms.CharField()
    tenantID = forms.CharField()

class NameForm(forms.Form):
    newVM = forms.CharField()
    imageName = forms.CharField()
    flavorName = forms.CharField()

class EditForm(forms.Form):
    VM_id = forms.CharField()
    flavor_id = forms.CharField()

class ControlForm(forms.Form):
    VM_id = forms.CharField()
    action = forms.CharField()
