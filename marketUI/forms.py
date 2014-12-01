from django import forms

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
