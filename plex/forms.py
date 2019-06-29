from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Invitation
from .plex import getSections, sectionKeys


class addForm(forms.Form):
    plex_token = forms.CharField(widget=forms.HiddenInput())
    invitation = forms.CharField(widget=forms.HiddenInput())


class invitationAdminForm(forms.ModelForm):
    choices = list(map(lambda x: [x.key, x.title], getSections()))
    libraries = forms.MultipleChoiceField(
        label=_('Libraries'),
        choices=choices,
        widget=forms.CheckboxSelectMultiple(),
        initial=sectionKeys)

    class Meta:
        model = Invitation
        fields = '__all__'

    def clean_libraries(self):
        if len(self.cleaned_data['libraries']) < 1:
            raise forms.ValidationError('Select at least 1.')
        return self.cleaned_data['libraries']
