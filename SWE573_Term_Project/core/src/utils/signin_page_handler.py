from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from . import user_model_handler


def signin_page_handler_main(request):
    if request.method == "GET":
        return signin_get_method_handler(request=request)
    elif request.method == "POST":
        return signin_post_method_handler(request=request)
    else:
        # TODO - Dağlar: Review here when homepage is created
        return render(request, "homepage.html")


def signin_get_method_handler(request):
    return render(request, "signin.html")

def signin_post_method_handler(request):
    is_validated = validate_signin_form(request=request)
    if is_validated:
        return redirect("core:profile")
    else:
        return HttpResponseRedirect("/signin")


def validate_signin_form(request):
    username = request.POST["username"]
    password = request.POST["password"]
    # Validate username is not exist
    if user_model_handler.validate_username(username=username):
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