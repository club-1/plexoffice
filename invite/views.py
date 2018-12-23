from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from plexapi.myplex import MyPlexAccount, BadRequest
from .forms import addForm


def home(request):
    form = addForm(request.POST or None)
    return render(request, 'invite/home.html', {'form': form})


def confirm(request):
    return render(request, 'invite/confirm.html')


def listUsers(request):
    account = MyPlexAccount(settings.PLEX['LOGIN'], settings.PLEX['PASSWORD'])
    users = account.users()
    return render(request, 'invite/listUsers.html', {'users': users})


def addFriend(request):
    form = addForm(request.POST)
    if form.is_valid():
        account = MyPlexAccount(
            settings.PLEX['LOGIN'],
            settings.PLEX['PASSWORD'])
        try:
            account.inviteFriend(
                form.cleaned_data['email'],
                'b9920c8e436c79b55d89c46e51c9e832059ec292',
                ['4', '5', '6', '7']
            )
            return redirect('invite-confirm')
        except BadRequest:
            messages.error(
                request,
                'L\'accès a déjà été accordé à cette adresse email')
        except Exception as e:
            messages.error(request, 'Internal error: ' + e)
    return redirect('invite-home')
