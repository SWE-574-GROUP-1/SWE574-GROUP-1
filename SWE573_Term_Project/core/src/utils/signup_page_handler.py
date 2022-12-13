import string
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from . import user_model_handler, profile_model_handler


def signup_page_handler_main(request):
    if request.method == "GET":
        print("Get method is called")
        return signup_get_method_handler(request=request)
    elif request.method == "POST":
        print("Post method is called")
        return signup_post_method_handler(request=request)
    else:
        return render(request, "homepage.html")


def signup_get_method_handler(request):
    return render(request, "signup.html")


def signup_post_method_handler(request):
    print
    # Get form data
    # validate the form
    is_validated = validate_signup_form(request=request)
    if is_validated:
        print("signup form is validated")
        user_model_handler.create_user(request=request)
        profile_model_handler.create_profile(request=request)
        return user_model_handler.login_user(request=request)
    else:
        return redirect('core:signup')


def validate_signup_form(request) -> bool:
    username = request.POST.get("username")
    email = request.POST.get("email")
    # validate username, email, password
    if not user_model_handler.validate_username(username=username):
        print("Signup form 1")
        messages.info(request, "Username is already exist.")
        return False
    if not user_model_handler.validate_email(email=email):
        print("Signup form 2")
        messages.info(request, "Email is already exists.")
        return False
    if not validate_password(request=request):
        print("Signup form 3")
        return False
    else:
        print("Signup form 4")
        return True


def validate_password(request):
    # Get passwords from post
    password = request.POST.get("password")
    password2 = request.POST.get("password2")
    # Equality validation
    if password != password2:
        messages.info(request, "Passwords do not match!")
        return False
    # Validate password format
    elif not validate_password_format(request=request, password=password):
        return False
    else:
        return True

def validate_password_format(request, password: str):
    # Set allowed characters
    hard_coded_set_of_allowed_characters = set(string.ascii_letters + string.digits + '@#$%^&+=')
    # Set allowed minimum length
    allowed_min_length = 8
    if len(password) < allowed_min_length:
        print("Length is false")
        messages.info(request, "Password must contain at least 8 elements!")
        return False
    # Allowed char validation
    elif any(passChar not in hard_coded_set_of_allowed_characters for passChar in password):
        print("Illegal chars")
        messages.info(request, "Password contains illegal characters!")
        return False
    else:
        return True

