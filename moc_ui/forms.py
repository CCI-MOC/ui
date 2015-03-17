from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    auth_url = forms.CharField()

class UserRegisterForm(forms.Form):
    userName = forms.CharField()
    password = forms.CharField()
    confirm_password = forms.CharField()
    Email = forms.CharField(required=False)

class UserAddForm(forms.Form):
    userName = forms.CharField()
    roleName = forms.CharField()

class UserRemoveForm(forms.Form):
    userName = forms.CharField()

class RoleEditForm(forms.Form):
    userName = forms.CharField()
    editAction = forms.CharField()
    roleName = forms.CharField()

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
