from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path("", views.index, name = "index"),
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name = "logout"),
    path("register", views.register, name = "register"),
    path("profile/<str:username>", views.profile, name = "profile"),
    path("profile/change/<str:username>", views.profile_change, name = "edit")
]
