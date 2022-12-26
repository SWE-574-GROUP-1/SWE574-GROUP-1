from django.contrib.auth.decorators import login_required
from .src.pages.profile_page_handler import profile_page_handler_main
from .src.models.post_model_handler import __delete_post__, __book_post__
from .src.pages.signup_page_handler import signup_page_handler_main
from .src.pages.signin_page_handler import signin_page_handler_main
from .src.models.user_model_handler import *
from .src.pages.settings_page_handler import settings_page_handler_main
from .models import Profile


@login_required(login_url="core:signin")
def feed(request: object):
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
