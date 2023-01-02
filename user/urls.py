from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template="users/login.html"), name="user-login"),
    path('logout/', auth_views.LogoutView.as_view(template="users/login.html"), name="user-logout"),
]
