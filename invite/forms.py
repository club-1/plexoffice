from django import forms


class addForm(forms.Form):
    email = forms.EmailField(label="Email")
    token = forms.CharField(widget=forms.HiddenInput())
