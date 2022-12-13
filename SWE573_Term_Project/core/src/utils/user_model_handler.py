from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

def create_user(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    pass


def login_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    redirect_path = request.META.get('HTTP_REFERER')
    try:
    # Log user in and redirect to feed
        user_login = auth.authenticate(username=username, password=password)
        auth.login(request, user_login)
        return redirect("core:profile")
    except Exception as e:
        messages.info(request, f"Username or Password is invalid. Error: {e}")
        return HttpResponseRedirect(redirect_path)


def delete_user(request):
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
    # Get the user
    user = User.objects.get(username=old_username)
    # Set the username
    user.username = new_username
    # Save the user with new username
    user.save()

def email_setter(username: str, new_email: str):
    # Get the user
    user = User.objects.get(username=username)
    # Set the email
    user.email = new_email
    # Save the user with new username
    user.save()

def validate_username(username: str) -> bool:
    if User.objects.filter(username=username).exists():
        return False
    else:
        return True


def validate_email(email: str) -> bool:
    if User.objects.filter(email=email).exists():
        return False
    else:
        return True