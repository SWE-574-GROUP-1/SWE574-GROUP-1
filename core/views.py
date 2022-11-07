from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User, auth

from .models import Profile
from .forms import NewUserForm
# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

def signup(request):
    if request.method == "GET":
        return render(request, "signup.html")
    
    elif request.method == "POST":
        # Collect form data
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email is already exists.")
                return redirect("core:signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username is already exist.")
                return redirect("core:signup")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # TODO: Log user in and redirect to homepage or complete profile page
                user_model = User.objects.get(username=username)
                # Create profile object for the new user
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect("core:signup") # TODO: CHANGE TO SIGNIN
        else:
            messages.info(request, "Passwords do not match!")
            return redirect(to='core:signup')
    else:
        return render(request, "homepage.html")
    
def signin(request):
    pass