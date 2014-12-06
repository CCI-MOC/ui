from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class TenantLoginForm(forms.Form):
    tenantName = forms.CharField()
    tenantID = forms.CharField()

class TenantCreateForm(forms.Form):
    tenantName = forms.CharField()
    tenantDesc = forms.CharField(required=False)

class VMCreateForm(forms.Form):
    newVM = forms.CharField()
    imageName = forms.CharField()
    flavorName = forms.CharField()

class VMEditForm(forms.Form):
    VM_id = forms.CharField()
    flavor_id = forms.CharField()

class VMControlForm(forms.Form):
    VM_id = forms.CharField()
    action = forms.CharField()
