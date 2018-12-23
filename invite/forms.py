from django import forms


class addForm(forms.Form):
    email = forms.EmailField(label="Email")
