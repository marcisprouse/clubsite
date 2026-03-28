from django import forms

class SearchHomeForm(forms.Form):
    query = forms.CharField(label="")