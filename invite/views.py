from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.utils import timezone

from plexapi.myplex import MyPlexAccount, PlexServer, BadRequest
from .forms import addForm
from .models import Token


def home(request, tokenString=''):
    form = addForm(None)
    token = get_object_or_404(Token, string=tokenString)
    if token.date_usage != None:
        return redirect('invite-expired')
    form.fields['token'].initial = tokenString
    return render(request, 'invite/home.html', {'form': form})


def confirm(request):
    return render(request, 'invite/confirm.html')


def expired(request):
    return render(request, 'invite/expired.html')


def listUsers(request):
    account = MyPlexAccount(settings.PLEX['LOGIN'], settings.PLEX['PASSWORD'])
    users = account.users()
    return render(request, 'invite/listUsers.html', {'users': users})


def listSections(request):
    account = MyPlexAccount(settings.PLEX['LOGIN'], settings.PLEX['PASSWORD'])
    plex = PlexServer(settings.PLEX['URL'], account._token)
    sections = plex.library.sections()
    return render(request, 'invite/listSections.html', {'sections': sections})


def addFriend(request):
    form = addForm(request.POST)
    tokenString = ''
    if form.is_valid():
        tokenString = form.cleaned_data['token']
        token = get_object_or_404(Token, string=tokenString)
        if token.date_usage != None:
            return redirect('invite-expired')
        account = MyPlexAccount(
            settings.PLEX['LOGIN'],
            settings.PLEX['PASSWORD'])
        try:
            email = form.cleaned_data['email']
            account.inviteFriend(
                email,
                settings.PLEX['SERVER'],
                token.sections
            )
            token.date_usage = timezone.now()
            token.used_by = email
            token.save()
            return redirect('invite-confirm')
        except BadRequest:
            messages.error(
                request,
                'L\'accès a déjà été accordé à cette adresse email')
        except Exception as e:
            messages.error(request, 'Internal error: ' + e)
    return redirect('invite-home', tokenString)
