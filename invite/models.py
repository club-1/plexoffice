from django.db import models
from django.utils import timezone
from django.shortcuts import redirect
import hashlib
from time import time


class Token(models.Model):
    string = models.CharField(
        default=hashlib.sha1(str(time()).encode()).hexdigest(),
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

    class Meta:
        verbose_name = "token"
        ordering = ['date_creation']

    def __str__(self):
        return self.string

    def share_url(self):
        return redirect('invite-home', self.string).url
