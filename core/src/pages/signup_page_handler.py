"""Contains utility methods to manage signup.html"""
import string
from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import profile_model_handler, user_model_handler


def signup_page_handler_main(request: object) -> redirect:
    """
    Implementation of main method to manage requests from signup.html
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: Redirects the user
    """
    if request.method == "GET":
        print("Get method is called")
        return signup_get_method_handler(request=request)
    elif request.method == "POST":
        print("Post method is called")
        return signup_post_method_handler(request=request)
    else:
        return render(request, "homepage.html")


def signup_get_method_handler(request: object) -> render:
    """
    Implementation of managing get requests from signup.html
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: Renders the signup page
    """
    return render(request, "signup.html")


def signup_post_method_handler(request: object) -> redirect:
    """
    Implementation of managing post requests from signup.html. Checks the validity of the signup form and redirects
    accordingly
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: Redirects the user
    """

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


def validate_signup_form(request: object) -> bool:
    """
    Implementation of validating form received from signup.html
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: bool, True if the form is valid else False
    """
    username = request.POST.get("username")
    email = request.POST.get("email")
    # validate username, email, password
    if not user_model_handler.validate_availability_username(username=username):
        print("Signup form 1")
        messages.info(request, "Username is already exist.")
        return False
    if not user_model_handler.validate_availability_email(email=email):
        print("Signup form 2")
        messages.info(request, "Email is already exists.")
        return False
    if not validate_password(request=request):
        print("Signup form 3")
        return False
    else:
        print("Signup form 4")
        return True


def validate_password(request: object) -> bool:
    """
    Implementation of validating password. Compares whether 2 passwords are equal then checks its validity
    to default passwords format
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: a boolean, True if password is valid, False if invalid
    """
    # Get passwords from post
    password = request.POST.get("password")
    password2 = request.POST.get("password2")
    # Equality validation
    if password != password2:
        messages.info(request, "Passwords do not match!")
        return False
    elif not validate_password_length(password=password):
        messages.info(request, "Password must contain at least 8 elements!")
        return False
    # Validate password format
    elif not validate_password_format(password=password):
        messages.info(request, "Password contains illegal characters!")
        return False
    else:
        return True


def validate_password_length(password: str, allowed_min_length: int = 8) -> bool:
    """
    Implementation of validating password length greater than 8
    @param password: string, that corresponds to the password
    @param allowed_min_length: integer, that corresponds to minimum allowable length of a password, 8 char by default
    @return: boolean, True if password length is valid, otherwise False
    """
    # TODO - Dağlar: Decide on migrating password handling to another file?
    # Set allowed minimum length
    allowed_min_length = allowed_min_length
    if len(password) < allowed_min_length:
        print("Length is false")
        return False
    else:
        return True


def validate_password_format(password: str):
    """
    Implementation of validating password regex format
    @param password: a string, that corresponds to the password
    @return: a boolean, True if password format is valid, otherwise False
    """
    # TODO - Dağlar: Decide on migrating password handling to another file?
    # Set allowed characters
    hard_coded_set_of_allowed_characters = set(string.ascii_letters + string.digits + '@#$%^&+=')
    # Allowed char validation
    if any(passChar not in hard_coded_set_of_allowed_characters for passChar in password):
        print("Illegal chars")
        return False
    else:
        return True
