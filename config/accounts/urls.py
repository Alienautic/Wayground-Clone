from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/", views.profile_view, name="profile"),
]