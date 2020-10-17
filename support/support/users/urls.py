from django.urls import path
from . import views
from .views import (AccountDetailView,
                    ProfileFollowAPIToggle, ProfileFollowToggle)
app_name = 'users'

urlpatterns = [
    path('profile/register/', views.signup, name='register'),
    path('profile/edit/', views.profile, name='profile'),
    path('user/<slug:slug>/', AccountDetailView.as_view(), name='profilepage'),
    path('user/<slug:slug>/follow/',
         ProfileFollowToggle.as_view(),
         name='profile-follow-toggle'),
    path('api/user/<slug:slug>/follow/',
         ProfileFollowAPIToggle.as_view(),
         name='profile-follow-api-toggle'),
]
