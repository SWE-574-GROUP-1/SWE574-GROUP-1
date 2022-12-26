"""Contains utility methods to manage profile.html"""
from django.http import HttpResponseRedirect
from ...models import Profile, Post, Tag
from django.shortcuts import render
from ..models import post_model_handler
from django.contrib.auth.models import User


def profile_page_handler_main(request: object, profile_owner_username: str) -> HttpResponseRedirect:
    """
    Implementation of main method to manage requests from profile.html
    @param profile_owner_username: owner_username attribute of the profile object
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: Redirects the user
    """
    print("Profile handler is called")
    if request.method == "POST":
        return profile_post_method_handler(request=request)
    elif request.method == "GET":
        return profile_get_method_handler(request=request, profile_owner_username=profile_owner_username)
    else:
        raise "Invalid HTTP Method"


def profile_get_method_handler(request: object, profile_owner_username: str) -> render:
    """
    Implementation of managing get requests from profile.html. Fetches the Profile and Post models of user and
    sends them to frontend
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @param profile_owner_username: username of the profile object to be displayed
    @return: Renders the profile page with Profile and Post data
    """
    # Get the profile owner user object and profile
    profile_owner_user_object = User.objects.get(username=profile_owner_username)
    profile_owner_user_profile = Profile.objects.get(user=profile_owner_user_object)
    # Get the request owner user object and profile
    request_owner_user_object = User.objects.get(username=request.user.username)
    request_owner_user_profile = Profile.objects.get(user=request_owner_user_object)
    profile_owner_posts = Post.objects.filter(owner_username=profile_owner_user_object).order_by('-created_at')
    context = {'request_owner_user': request_owner_user_object,
               'request_owner_user_profile': request_owner_user_profile,
               'profile_owner_user': profile_owner_user_object,
               'profile_owner_user_profile': profile_owner_user_profile,
               'posts': profile_owner_posts,
               'num_followers': len(profile_owner_user_profile.followers),
               'num_following': len(profile_owner_user_profile.following),
               'num_posts': len(Post.objects.filter(owner_username=profile_owner_user_profile.user.username)),
               'available_tags': Tag.objects.all(),
    }
    print(f"profile_owner_username is: {profile_owner_user_object.username}")
    print(f"request_owner_username is: {request_owner_user_object.username}")
    return render(request, "profile.html", context=context)


def profile_post_method_handler(request: object) -> HttpResponseRedirect:
    """
    Implementation of managing post requests from profile.html. Checks the form_name within the request and calls
    corresponding functions for given form_name
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: Redirects the user
    """
    redirect_path = request.META.get('HTTP_REFERER')
    if request.POST.get("form_name") == "post-create-form":
        print("post-create-form received")
        post_model_handler.create_post(request=request)
    elif request.POST.get("form_name") == "post-update-form":
        print("post-update-form received")
        post_model_handler.update_post(request=request)
    elif request.POST.get("form-name") == "settings-form":
        # TODO - Dağlar: Fill here when you insert settings into profile
        pass
    else:
        raise f"Invalid form-name: {request.POST.get('form-name')}"
    return HttpResponseRedirect(redirect_path)
