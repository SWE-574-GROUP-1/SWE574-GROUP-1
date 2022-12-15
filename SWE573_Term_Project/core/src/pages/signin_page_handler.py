"""Contains utility methods to manage signin.html"""
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import auth
from ..models import user_model_handler


def signin_page_handler_main(request: object) -> redirect:
    """
    Implementation of main method to manage requests from signin.html
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: Redirects the user
    """
    if request.method == "GET":
        return signin_get_method_handler(request=request)
    elif request.method == "POST":
        return signin_post_method_handler(request=request)
    else:
        # TODO - Dağlar: Review here when homepage is created
        return render(request, "homepage.html")


def signin_get_method_handler(request: object) -> render:
    """
    Implementation of managing get requests from signin.html
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: Renders the profile page with Profile and Post data
    """
    return render(request, "signin.html")


def signin_post_method_handler(request: object) -> [redirect, HttpResponseRedirect]:
    """
    Implementation of managing post requests from signin.html
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: Logs in the user if the signin for valid else redirects to the signin page
    """

    is_validated = validate_signin_form(request=request)
    if is_validated:
        return redirect("core:profile")
    else:
        return HttpResponseRedirect("/signin")


def validate_signin_form(request: object) -> bool:
    """
    Implementation of validating form received from signin.html
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: bool, True if the form is valid else False
    """
    username = request.POST["username"]
    password = request.POST["password"]
    # Validate username is not exist
    if user_model_handler.validate_availability_username(username=username):
        messages.info(request, "Username does not exist.")
        return False
    # Authenticate username + password
    try:
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        return True
    except Exception as e:
        messages.info(request, f"Invalid password. Error: {e}")
        return False
