from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import NewUserForm
# Create your views here.

@login_required(login_url="core:signin")
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
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username is already exist.")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email is already exists.")
                return redirect("core:signup")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # TODO: Log user in and redirect to homepage or complete profile page
                user_model = User.objects.get(username=username)
                # Create profile object for the new user
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect("core:signin")
        else:
            messages.info(request, "Passwords do not match!")
            return redirect(to='core:signup')
    else:
        return render(request, "homepage.html")

def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("core:homepage")
        else:
            messages.info(request, "Username or Password is invalid.")
            return redirect("core:signin")
    else:
        return render(request, "signin.html")

@login_required(login_url="core:signin")
def logout(request):
    auth.logout(request)
    return redirect("core:signin")

def root(request):
    if request.method == "GET":
        return render(request, "root.html")