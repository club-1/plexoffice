from django.db import models
from django.utils import timezone
from django.shortcuts import resolve_url
from django.utils.translation import gettext_lazy as _
from .plex import sectionKey2Title

import jsonfield
from hashlib import sha1
from time import time


def gen_string():
    return sha1(str(time()).encode()).hexdigest()


class Invitation(models.Model):
    token = models.CharField(
        default=gen_string,
        max_length=255,
        verbose_name=_('Token'))
    date_creation = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Creation date'))
    date_usage = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Usage date'))
    used_by = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('Used by'))
    libraries = jsonfield.JSONField(verbose_name=_('Libraries'))
    sent_to = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('Sent to'))

    class Meta:
        verbose_name = _('Invitation')
        ordering = ['date_creation']

    def __str__(self):
        return self.token

    def sent(self):
        return self.sent_to is not None

    def share_url(self):
        return resolve_url('plex-invite-home', self.token)

    def title_libraries(self):
        return list(map(lambda x: sectionKey2Title(x), self.libraries))
    title_libraries.short_description = _('Libraries')

    def nb_libraries(self):
        return len(self.libraries)
    nb_libraries.short_description = _('Libraries')
