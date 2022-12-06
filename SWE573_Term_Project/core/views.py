from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User, auth 
from django.contrib.auth.decorators import login_required

from .models import Profile, Post
from .forms import NewUserForm
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

@login_required(login_url="core:signin")
def feed(request):
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
                # Log user in and redirect to feed
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                
                # Create profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect("core:profile")
        else:
            messages.info(request, "Passwords do not match!")
            return redirect(to='core:signup')
    else:
        return render(request, "homepage.html")

def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if not User.objects.filter(username=username).exists():
            messages.info(request, "Username does not exist.")
            return HttpResponseRedirect("/signin")
        try:
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect("core:profile")
        except Exception as e:
            messages.info(request, "Username or Password is invalid. Error: {e}")
            return redirect("core:signin")
    else:
        return render(request, "signin.html")

@login_required(login_url='core:signin')
def settings(request):
    # TODO: Better implementation of this method
    user_profile = Profile.objects.get(user=request.user)
    user = User.objects.get(username=request.user.username)
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
    return redirect("core:signin")

    
@login_required(login_url="core:signin")
def delete_account(request):
    try:
        # Delete the User
        user_object = User.objects.get(username = request.user.username)
        user_object.delete()
        messages.success(request, "The user is deleted")            
    except User.DoesNotExist:
        messages.error(request, "User does not exist")    
        return render(request, 'settings_1.html')
    except Exception as e: 
        return render(request, 'feed.html',{'err':e.message})

    return render(request, 'signup.html')

@login_required(login_url="core:signin")
def change_password(request):
    user_object = User.objects.get(username = request.user.username)
    # if password == password2:
    # user_profile = Profile.objects.get(user=user_object)
    pass

@login_required(login_url="core:signin")
def upload_post(request):
    pass


@login_required(login_url="core:signin")
def profile(request):
    user_profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(owner_username=request.user.username)
    print(request.POST)
    if request.method == "POST":
        owner_username = request.user.username
        if request.POST.get("form_name") == "post-form":
            
            new_post = Post.objects.create(owner_username=owner_username,
                                           link=request.POST.get("link"),
                                           caption=request.POST.get("caption"))
            new_post.save()
            return HttpResponseRedirect("/profile")
            # return render(request, "profile.html", {'user_profile': user_profile, 'posts': posts})
    return render(request, "profile.html", {'user_profile': user_profile, 'posts': posts})
