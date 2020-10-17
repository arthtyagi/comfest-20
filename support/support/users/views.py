from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.core.mail import send_mail 

from .models import User, Profile

def index(request):
    return render(request, "index.html")
    
def login_view(request):
    
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)

        # Check if authentication was successful
        if user is not None:
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect(forum:list)
        else:
            return render(request, "users/login.html", {
                "error_message": "Invalid email and/or password."
            })
            
    else: # request.method == 'GET'
        return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST['last_name']
        email = request.POST["email"]
        username = request.POST['username']

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "users/register.html", {
                "error_message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(first_name = first_name, last_name = last_name, username = username, email = email, password = password)
            user.save()
            profile = Profile(user = user)
            profile.save()
        
        #repeated email
        except IntegrityError:
            return render(request, "users/register.html", {
                "error_message": "Email already in use."
            })
        
        #if no error occurs, the user is logged in
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(forum:list)
    
    else: # request.method == 'GET'
        return render(request, "users/register.html")

def profile(request, username):
    user = User.objects.get(username = username)
    profile = Profile.objects.get(user = user)
    print(profile)
    return render(request, "users/profile.html", {
        "account": profile,
        "media_url": conf_settings.MEDIA_URL
    })   

def profile_change(request, username):
    
    if request.method == 'POST':
        
        user = request.user
        profile = Profile.objects.get(user=user)
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        image = request.POST['image']
        about = request.POST['about']
        
        user.first_name = first_name
        user.last_name = last_name
        profile.image = image
        profile.about = about
        
        user.save()
        profile.save()
        
        return redirect('profile', username = user.username)
    
    profile = Profile.objects.get(user = request.user)
    
    if not(profile.user == request.user):
        return redirect('profile', username = user.username)
    
    return render(request, 'users/profile_change.html', {
        'account': profile
    })