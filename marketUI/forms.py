from django import forms

class NameForm(forms.Form):
    newVM = forms.CharField()
