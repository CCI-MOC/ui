from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

class CreateClusterForm(forms.Form):
    auth_url = forms.CharField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

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
