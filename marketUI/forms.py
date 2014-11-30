from django import forms

class NameForm(forms.Form):
    newVM = forms.CharField()
    imageName = forms.CharField()
    flavorName = forms.CharField()
