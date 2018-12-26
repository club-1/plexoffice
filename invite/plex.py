from django.conf import settings
from plexapi.myplex import MyPlexAccount, PlexServer, BadRequest

account = None
server = None
sections = None


def getAccount():
    global account
    if account == None:
        account = MyPlexAccount(
            settings.PLEX['LOGIN'],
            settings.PLEX['PASSWORD'])
    return account


def getServer():
    global server
    if server == None:
        account = getAccount()
        server = PlexServer(settings.PLEX['URL'], account._token)
    return server


def getSections():
    global sections
    if sections == None:
        server = getServer()
        section = server.library.sections()
    return section


def sectionKey2Title(key):
    sections = getSections()
    for section in sections:
        if section.key == key:
            return section.title


def inviteFriend(email, sections):
    account = getAccount()
    account.inviteFriend(
        email,
        settings.PLEX['SERVER']
    )
