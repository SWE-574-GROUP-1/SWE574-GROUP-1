"""Contains utility methods to control settings.html"""
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from ...models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
from ..models import user_model_handler
from .signup_page_handler import validate_password_format


def settings_page_handler_main(request: object):
    """
    Implementation of main method to manage requests from settings.html
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: Redirects the user
    """
    if request.method == 'POST':
        return settings_page_post_handler(request=request)
    elif request.method == 'GET':
        return settings_page_get_handler(request=request)
    else:
        raise "Invalid HTTP Method"


def settings_page_get_handler(request: object) -> render:
    """
    Implementation of managing get requests from settings.html. Fetches the Profile model of user and
    sends them to frontend
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: Renders the profile page with Profile data
    """
    user_profile = Profile.objects.get(user=request.user)
    return render(request, 'settings.html', {'user_profile': user_profile})

def settings_page_post_handler(request: object) -> redirect:
    """
    Implementation of managing post requests from settings.html. Checks the form_name within the request and calls
    corresponding functions for given form_name
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: Redirects the user
    """
    # Profile information
    print(request.POST)
    if request.POST.get("form_name") == 'profile-information-form':
        # Pass the data to setter
        profile_information_setter(request=request)
        return redirect('core:settings')
    # Account Settings
    elif request.POST.get("form_name") == 'account-settings-form':
        # Pass the data to setter
        account_settings_setter(request=request)
        return redirect('core:settings')
    else:
        raise f"Invalid form name {request.POST.form_name}"


def profile_information_setter(request: object) -> None:
    """
    Implementation of profile information form setter. Checks the input data in form and
    performs required operation if data exist in form
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: None
    """
    user_profile = Profile.objects.get(user=request.user)
    if request.FILES.get('image'):
        user_profile.profile_image = request.FILES.get('image')
    # Set the bio
    if request.POST.get('bio'):
        user_profile.bio = request.POST.get('bio')
    # Save the user profile
    user_profile.save()
    pass


def account_settings_setter(request: object) -> redirect:
    """
    Implementation of account setting form setter. Checks the input data in form and
    performs required operation if data exist in form
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: Redirects the user to corresponding page
    """
    # TODO - Dağlar: Refactor here
    if request.POST.get("email"):
        username = request.user.username
        new_email = request.POST.get("email")
        if not user_model_handler.validate_availability_email(email=new_email):
            messages.info(request, "Email is already exist.")
        else:
            user_model_handler.email_setter(username=username, new_email=new_email)
    if request.POST.get("username"):
        old_username = request.user.username
        new_username = request.POST.get("username")
        # Validate that username is available
        if not user_model_handler.validate_availability_username(username=new_username):
            messages.info(request, "Username is already exist.")
        else:
            user_model_handler.username_setter(old_username=old_username, new_username=new_username)
    # Set the password
    if request.POST.get("old_password") and request.POST.get("new_password") and request.POST.get("new_password_2"):
        if request.POST.get("old_password") != request.POST.get("new_password") == request.POST.get("new_password_2"):
            try:
                # Get the user
                user = User.objects.get(username=request.user.username)
            except ObjectDoesNotExist:
                new_username = request.POST.get("username")
                user = User.objects.get(username=new_username)
            # Check password format
            if not  validate_password_format(request=request, password=request.POST.get("new_password")):
                return redirect('core:settings')
            # Compare with current password
            elif user.check_password(request.POST.get("old_password")):
                # Set the password
                user.set_password(request.POST.get("new_password"))
                messages.info(request, "Password successfully changed.")
                user.save()
                print("Password changed")
                messages.info(request, "Password changed")
                # TODO: Should I logout the user, when i change the password?
                return redirect('core:signin')
            else:
                messages.info(request, "Invalid old password")
        elif request.POST.get("new_password") != request.POST.get("new_password2"):
            messages.info(request, "New Passwords do not match!")
        else:
            messages.info(request, "Unknown error while setting new password, please try again.")
    return redirect('core:settings')

