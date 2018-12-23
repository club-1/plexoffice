from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='invite-home'),
    path('add', views.addFriend, name='invite-add'),
    path('confirm', views.confirm, name='invite-confirm'),
    path('users', views.listUsers, name="invite-users-list")
]