from django.urls import path
from . import views

urlpatterns = [
    path('token/<str:tokenString>', views.home, name='invite-home'),
    path('add', views.addFriend, name='invite-add'),
    path('confirm', views.confirm, name='invite-confirm'),
    path('expired', views.expired, name='invite-expired'),
    path('users', views.listUsers, name="invite-users-list"),
]
