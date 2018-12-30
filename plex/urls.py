from django.urls import path
from . import views

urlpatterns = [
    path('invite/token/<str:invitationToken>', views.invite, name='plex-invite-home'),
    path('invite/add', views.addFriend, name='plex-invite-add'),
    path('invite/confirm', views.confirm, name='plex-invite-confirm'),
    path('invite/expired', views.expired, name='plex-invite-expired'),
    # path('users', views.listUsers, name='plex-users-list'),
    # path('sections', views.listSections, name='plex-sections-list'),
]
