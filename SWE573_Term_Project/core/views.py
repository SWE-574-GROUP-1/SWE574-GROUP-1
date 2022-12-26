from django.contrib.auth.decorators import login_required
from .src.pages.profile_page_handler import profile_page_handler_main
from .src.models.post_model_handler import __delete_post__, __book_post__
from .src.pages.signup_page_handler import signup_page_handler_main
from .src.pages.signin_page_handler import signin_page_handler_main
from .src.models.user_model_handler import *
from .src.pages.settings_page_handler import settings_page_handler_main
# TODO: Improve modularity
from .models import Profile
from django.http import HttpResponseRedirect

@login_required(login_url="core:signin")
def feed(request: object):
    # TODO: Fix this
    return render(request, 'test.html')


def signup(request: object):
    return signup_page_handler_main(request=request)


def signin(request: object):
    return signin_page_handler_main(request=request)


@login_required(login_url='core:signin')
def settings(request: object):
    return settings_page_handler_main(request=request)


@login_required(login_url="core:signin")
def logout(request: object):
    auth.logout(request)
    # TODO - Dağlar: Change this to homepage when created
    return redirect("core:signin")


@login_required(login_url="core:signin")
def delete_account(request: object):
    return delete_user(request=request)


@login_required(login_url='core:signin')
def delete_post(request: object):
    return __delete_post__(request=request)


@login_required(login_url='core:signin')
def book_post(request: object):
    return __book_post__(request=request)


@login_required(login_url="core:signin")
def profile(request, profile_owner_username):
    return profile_page_handler_main(request=request, profile_owner_username=profile_owner_username)


@login_required(login_url="core:signin")
def search(request: object):
    # Get the request owner user object and profile
    request_owner_user_object = User.objects.get(username=request.user.username)
    request_owner_user_profile = Profile.objects.get(user=request_owner_user_object)
    context = {
        "request_owner_user": request_owner_user_object,
        "request_owner_user_profile": request_owner_user_profile,
    }
    # Get the keyword to search
    if request.method == 'POST':
        keyword = request.POST.get("keyword")
        if keyword:
            searched_user_objects = User.objects.filter(username__icontains=keyword)
            search_result_user_profiles = list()
            for user in searched_user_objects:
                profile_object = Profile.objects.get(user=user)
                search_result_user_profiles.append(profile_object)
                print(profile_object.user.username)
            # TODO: Implement search for tags and spaces too
            # search_tag_objects =
            # searched_spaces_objects =
            print(f"{len(search_result_user_profiles)} users are found")
            context["search_result_user_profiles"] = search_result_user_profiles

    print("POST IS:")
    print(request.POST.get("keyword"))
    return render(request, "search.html", context=context)

@login_required(login_url="core:signin")
def follow(request: object):
    path = request.META.get('HTTP_REFERER')
    profile_owner_id_user = int(request.GET.get('profile_owner_id_user'))
    print("id_user obtained from request:", profile_owner_id_user, type(profile_owner_id_user))
    profile_owner_user_profile = Profile.objects.get(id_user=profile_owner_id_user)
    request_owner_user_profile = Profile.objects.get(user=request.user)
    print("profile_owner id_user is", profile_owner_user_profile.id_user, type(profile_owner_user_profile.id_user))
    print("reqeust_owner id_user is", request_owner_user_profile.id_user, type(request_owner_user_profile.id_user))
    print("Followers", profile_owner_user_profile.followers)
    # Remove follower/following
    if request_owner_user_profile.id_user in profile_owner_user_profile.followers:
        # Remove follower
        profile_owner_user_profile.followers.remove(request_owner_user_profile.id_user)
        # Remove following
        request_owner_user_profile.following.remove(profile_owner_user_profile.id_user)
        # Save profiles
        profile_owner_user_profile.save()
        request_owner_user_profile.save()
        print("unfollowed")

    # Add follower/following
    else:
        # Add follower
        profile_owner_user_profile.followers.append(request_owner_user_profile.id_user)
        # Add following
        request_owner_user_profile.following.append(profile_owner_user_profile.id_user)
        # Save profiles
        profile_owner_user_profile.save()
        request_owner_user_profile.save()
        print("followed")
    print("Followers of profile owner", profile_owner_user_profile.followers)
    return HttpResponseRedirect(path)
