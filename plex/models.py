from django.db import models
from django.utils import timezone
from django.shortcuts import redirect
from .plex import sectionKey2Title

import jsonfield
from hashlib import sha1
from time import time


def genString():
    return sha1(str(time()).encode()).hexdigest()


class Invitation(models.Model):
    token = models.CharField(
        default=genString,
        max_length=255)
    date_creation = models.DateTimeField(
        default=timezone.now,
        verbose_name="Creation date")
    date_usage = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Usage date")
    used_by = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    libraries = jsonfield.JSONField()
    sent_to = models.CharField(
        max_length=255,
        null=True,
        blank=True)

    class Meta:
        verbose_name = "invitation"
        ordering = ['date_creation']

    def __str__(self):
        return self.token

    def sent(self):
        return self.sent_to is not None

    def share_url(self):
        return redirect('plex-invite-home', self.token).url

    def title_libraries(self):
        return list(map(lambda x: sectionKey2Title(x), self.libraries))
    title_libraries.verbose_name = "libraries"

    def nb_libraries(self):
        return len(self.libraries)
    nb_libraries.verbose_name = "libraries"
