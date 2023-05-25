"""Contains utility methods for User model"""
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect


def create_user(request: object) -> None:
    """
    Implementation of creating a user model and saving it to database
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: None
    """
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    pass


def login_user(request: object) -> [redirect, HttpResponseRedirect]:
    """
    Implementation of authorizing the user to log in
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: Redirect to user to profile if authorized, otherwise refreshes the current page
    """
    username = request.POST.get("username")
    password = request.POST.get("password")
    redirect_path = request.META.get('HTTP_REFERER')
    try:
        # Log user in and redirect to feed
        user_login = auth.authenticate(username=username, password=password)
        auth.login(request, user_login)
        return redirect("core:profile", profile_owner_username=username)
    except Exception as e:
        messages.info(request, f"Username or Password is invalid. Error: {e}")
        return HttpResponseRedirect(redirect_path)


def delete_user(request: object) -> render:
    """
    Implementation of deleting a user from database. Checks whether user exist, if so deletes the user
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: renders a html page
    """
    username = request.user.username
    try:
        # Delete the User
        user_object = User.objects.get(username=username)
        user_object.delete()
        messages.success(request, "The user is deleted")
    except User.DoesNotExist:
        messages.error(request, "User does not exist")
        # TODO - Dağlar: Change this when settings is inserted to profile
        return render(request, 'settings_1.html')
    except Exception as e:
        return render(request, 'feed.html', {'err': e.message})
    # TODO - Dağlar: Change this to homepage(welcome page) when created
    return render(request, 'signup.html')


def username_setter(old_username: str, new_username: str) -> None:
    """
    Implementation of setter method for username attribute of the user
    @param old_username: a string, that corresponds to the old username
    @param new_username: a string, that corresponds to the new username
    @return: None
    """
    # Get the user
    user = User.objects.get(username=old_username)
    # Set the username
    user.username = new_username
    # Save the user with new username
    user.save()


def email_setter(username: str, new_email: str) -> None:
    """
    Implementation of setter method for email attribute of the user
    @param username: a string, that corresponds to the username attribute of the User model
    @param new_email: a string, that corresponds to the new email address to be set
    @return: None
    """
    # Get the usr
    user = User.objects.get(username=username)
    # Set the email
    user.email = new_email
    # Save the user with new username
    user.save()


def validate_availability_username(username: str) -> bool:
    """
    Implementation of validation of Username of User model
    @param username: a string that corresponds to username attribute of User object
    @return: True if username not exist, False if username already exist
    """
    if User.objects.filter(username=username).exists():
        return False
    else:
        return True


def validate_availability_email(email: str) -> bool:
    """
    Implementation of validation of email attribute of User model
    @param email: a string that corresponds to email attribute of User object
    @return: True if username not exist, False if username already exist
    """
    if User.objects.filter(email=email).exists():
        return False
    else:
        return True
