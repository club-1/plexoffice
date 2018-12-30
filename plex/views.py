from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.utils import timezone

from .plex import getAccount, getServer, getSections, inviteFriend
from plexapi.myplex import BadRequest, MyPlexAccount
from .forms import addForm
from .models import Invitation


def invite(request, invitationToken=''):
    form = addForm(None)
    invitation = get_object_or_404(Invitation, token=invitationToken)
    if invitation.date_usage != None:
        return redirect('plex-invite-expired')
    form.fields['invitation'].initial = invitationToken
    return render(request, 'plex/invite/home.html', {'form': form})


def confirm(request):
    return render(request, 'plex/invite/confirm.html')


def expired(request):
    return render(request, 'plex/invite/expired.html')


def listUsers(request):
    account = getAccount()
    users = account.users()
    return render(request, 'plex/listUsers.html', {'users': users})


def listSections(request):
    sections = getSections()
    return render(request, 'plex/listSections.html', {'sections': sections})


def addFriend(request):
    form = addForm(request.POST)
    invitationToken = ''
    if form.is_valid():
        invitationToken = form.cleaned_data['invitation']
        invitation = get_object_or_404(Invitation, token=invitationToken)
        if invitation.date_usage != None:
            return redirect('plex-invite-expired')
        try:
            plexToken = form.cleaned_data['plex_token']
            user = MyPlexAccount(token=plexToken)
            inviteFriend(user.email, invitation.libraries)
            invitation.date_usage = timezone.now()
            invitation.used_by = user.email
            invitation.save()
            return redirect('plex-invite-confirm')
        except BadRequest as e:
            print(e)
            messages.error(
                request,
                'L\'accès a déjà été accordé à cet utilisateur')
        except Exception as e:
            messages.error(request, 'Internal error: ' + e)
    return redirect('plex-invite-home', invitationToken)
