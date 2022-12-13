from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Profile, Post
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from django.shortcuts import render
from .src.utils.profile_page_handler import profile_page_handler_main
from .src.utils.post_model_handler import __delete_post__, __book_post__
from .src.utils.signup_page_handler import signup_page_handler_main
from .src.utils.signin_page_handler import signin_page_handler_main
from .src.utils.user_model_handler import *
from .src.utils.settings_page_handler import settings_page_handler_main

@login_required(login_url="core:signin")
def feed(request):
    return render(request, 'test.html')


def signup(request):
    return signup_page_handler_main(request=request)


def signin(request):
    return signin_page_handler_main(request=request)


@login_required(login_url='core:signin')
def settings(request):
    return settings_page_handler_main(request=request)
    # TODO: Better implementation of this method
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        # Set the image
        if request.FILES.get('image'):
            user_profile.profile_image = request.FILES.get('image')
        # Set the bio
        if request.POST.get('bio'):
            user_profile.bio = request.POST.get('bio')  
        # Set the email
        if request.POST.get("email"):
            if User.objects.filter(email=request.POST.get("email")).exists():
                messages.info(request, "Email is already exists.")
            else:
                # Get the user
                user = User.objects.get(username=request.user.username)
                # Set the email
                user.email = request.POST.get("email")
                # Save the user with new username
                user.save()
        # Set the username
        if request.POST.get("username"):
            if User.objects.filter(username=request.POST.get('username')).exists():
                messages.info(request, "Username is already exist.")
            else:
                # Get the user
                user = User.objects.get(username=request.user.username)
                # Set the username
                user.username = request.POST.get("username")
                # Save the user with new username
                user.save()
        # Set the password
        if request.POST.get("old_password") and request.POST.get("new_password") and request.POST.get("new_password_2"):
            if request.POST.get("old_password") != request.POST.get("new_password") == request.POST.get("new_password_2"):
                try:
                    # Get the user
                    user = User.objects.get(username=request.user.username)
                except ObjectDoesNotExist:
                    user = User.objects.get(username=request.POST.get("username"))
                # Compare with current password
                if user.check_password(request.POST.get("old_password")):
                    # Set the password
                    user.set_password(request.POST.get("new_password"))
                    messages.info(request, "Password succesfully changed.")
                    user.save()
                    print("Password changed")
                    # TODO: Should I logout the user, when i change the password?
                    return redirect('core:signin')
                else:
                    messages.info(request, "Invalid old password")
                    
            elif request.POST.get("old_password") != request.POST.get("old_password2"):
                messages.info(request, "New Passwords do not match!")
            else:
                messages.info(request, "Unknown error while setting new password, please try again.")

        # Save the user profile
        user_profile.save()
        # TODO: Think of this redirect you may use flags to logout user or refresh page
        return redirect('core:settings')
    return render(request, 'settings.html', {'user_profile': user_profile})


@login_required(login_url="core:signin")
def logout(request):
    auth.logout(request)
    # TODO - Dağlar: Change this to homepage when created
    return redirect("core:signin")

    
@login_required(login_url="core:signin")
def delete_account(request):
    return delete_user(request=request)


@login_required(login_url='core:signin')
def delete_post(request):
    return __delete_post__(request=request)


@login_required(login_url='core:signin')
def book_post(request):
    return __book_post__(request=request)


@login_required(login_url="core:signin")
def profile(request):
    return profile_page_handler_main(request=request)


