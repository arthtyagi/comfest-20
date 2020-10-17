from .models import Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.views.generic import DetailView, ListView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from support.mixins import PageTitleMixin
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


def signup(request):
    return render(request, "users/register.html", {'title': 'Register'})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'users/profile.html', context)


class AccountDetailView(PageTitleMixin, LoginRequiredMixin, DetailView):
    model = Profile
    title = 'User Profile'
    template_name = "users/profilepage.html"


"""

Follow Views below

AJAX to Follow/Unfollow a User using APIView

"""


class ProfileFollowToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        profile = get_object_or_404(Profile, slug=self.kwargs['slug'])
        slug = self.kwargs.get('slug')
        print(slug)
        obj = get_object_or_404(Profile, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.followers.all():
                obj.followers.remove(user)
            else:
                obj.followers.add(user)
        return url_


class ProfileFollowAPIToggle(APIView):
    authentication_classes = [
        SessionAuthentication,
    ]
    permission_clases = [
        IsAuthenticated,
    ]

    def get(self, request, slug=None, format=None):
        obj = get_object_or_404(Profile, slug=slug)
        updated = False
        liked = False
        user = self.request.user
        if user.is_authenticated:
            if user in obj.followers.all():
                liked = False
                obj.followers.remove(user)
            else:
                liked = True
                obj.followers.add(user)

            updated = True
        data = {'updated': updated, 'liked': liked}
        return Response(data)
