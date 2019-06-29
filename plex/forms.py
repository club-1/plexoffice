from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Invitation
from .plex import getSections, sectionKeys


class addForm(forms.Form):
    plex_token = forms.CharField(widget=forms.HiddenInput())
    invitation = forms.CharField(widget=forms.HiddenInput())


class invitationAdminForm(forms.ModelForm):
    libraryChoices = list(map(lambda x: [x.key, x.title], getSections()))
    libraries = forms.MultipleChoiceField(
        required=False,
        label=_('Libraries'),
        choices=libraryChoices,
        widget=forms.CheckboxSelectMultiple(),
        initial=sectionKeys)

    class Meta:
        model = Invitation
        fields = '__all__'
        widgets = {
            'token': forms.TextInput(attrs={'size':'50'})
        }

    def clean_libraries(self):
        if len(self.cleaned_data['libraries']) < 1:
            raise forms.ValidationError(_('Select at least 1.'))
        return self.cleaned_data['libraries']
