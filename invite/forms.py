from django import forms
from .plex import getSections


class addForm(forms.Form):
    email = forms.EmailField(label="Email")
    token = forms.CharField(widget=forms.HiddenInput())


class tokenAdminForm(forms.ModelForm):
    choices = list(map(lambda x: [x.key, x.title], getSections()))
    libraries = forms.MultipleChoiceField(
        choices=choices, widget=forms.CheckboxSelectMultiple())

    def clean_libraries(self):
        if len(self.cleaned_data['libraries']) < 1:
            raise forms.ValidationError('Select at least 1.')
        return self.cleaned_data['libraries']
