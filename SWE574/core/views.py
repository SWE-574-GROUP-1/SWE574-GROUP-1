from django.contrib.auth.decorators import login_required
from .src.pages.profile_page_handler import profile_page_handler_main
from .src.models.post_model_handler import __delete_post__, __book_post__
from .src.pages.signup_page_handler import signup_page_handler_main
from .src.pages.signin_page_handler import signin_page_handler_main
from .src.models.user_model_handler import *
from .src.pages.settings_page_handler import settings_page_handler_main
# TODO: Improve modularity
from django.urls import reverse
from .models import Profile, Tag, Space, Post
from django.http import HttpResponseRedirect
from .src.models import post_model_handler, tag_model_handler, space_model_handler
from itertools import chain


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
    request_owner_user_object = User.objects.get(
        username=request.user.username)
    request_owner_user_profile = Profile.objects.get(
        user=request_owner_user_object)
    context = {
        "request_owner_user": request_owner_user_object,
        "request_owner_user_profile": request_owner_user_profile,
    }
    # Get the keyword to search
    if request.method == 'POST':
        keyword = request.POST.get("keyword")
        if keyword:
            searched_user_objects = User.objects.filter(
                username__icontains=keyword)
            search_result_user_profiles = list()
            for user in searched_user_objects:
                profile_object = Profile.objects.get(user=user)
                search_result_user_profiles.append(profile_object)
                print(profile_object.user.username)
            # TODO: Implement search for posts, tags and spaces too
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
    print("id_user obtained from request:",
          profile_owner_id_user, type(profile_owner_id_user))
    profile_owner_user_profile = Profile.objects.get(
        id_user=profile_owner_id_user)
    request_owner_user_profile = Profile.objects.get(user=request.user)
    print("profile_owner id_user is", profile_owner_user_profile.id_user,
          type(profile_owner_user_profile.id_user))
    print("reqeust_owner id_user is", request_owner_user_profile.id_user,
          type(request_owner_user_profile.id_user))
    print("Followers", profile_owner_user_profile.followers)
    # Remove follower/following
    if request_owner_user_profile.id_user in profile_owner_user_profile.followers:
        # Remove follower
        profile_owner_user_profile.followers.remove(
            request_owner_user_profile.id_user)
        # Remove following
        request_owner_user_profile.following.remove(
            profile_owner_user_profile.id_user)
        # Save profiles
        profile_owner_user_profile.save()
        request_owner_user_profile.save()
        print("unfollowed")

    # Add follower/following
    else:
        # Add follower
        profile_owner_user_profile.followers.append(
            request_owner_user_profile.id_user)
        # Add following
        request_owner_user_profile.following.append(
            profile_owner_user_profile.id_user)
        # Save profiles
        profile_owner_user_profile.save()
        request_owner_user_profile.save()
        print("followed")
    print("Followers of profile owner", profile_owner_user_profile.followers)
    print(path)
    return HttpResponseRedirect(path)


def tags(request, tag_name):
    print(f"TAG NAME IS: {tag_name}")
    # Get the Tag object for given tag name
    try:
        tag = Tag.objects.get(name=tag_name)
    except Tag.DoesNotExist:
        path = request.META.get('HTTP_REFERER')
        # TODO: Add does not exist message here
        return HttpResponseRedirect(path)
    # Get all posts with specific tag name
    posts = tag.posts.all().order_by('-created')
    if request.method == 'POST':
        if request.POST.get('form_name') == 'tag-search-form':
            print(request.POST)
            tag_name = request.POST.get('tag_name_to_be_searched')
    # Create list of post owners
    post_owner_profile_list = list()
    for post in posts:
        user_obj = User.objects.get(username=post.owner_username)
        profile_obj = Profile.objects.get(user=user_obj)
        post_owner_profile_list.append(profile_obj)
        print(profile_obj.profile_image.url)
    request_owner_user_object = User.objects.get(username=request.user.username)
    request_owner_user_profile = Profile.objects.get(user=request_owner_user_object)
    post_owner_profile_list_with_posts = zip(post_owner_profile_list, posts)
    context = {"post_owner_profile_list_with_posts": post_owner_profile_list_with_posts,
               "request_owner_user_profile": request_owner_user_profile,
               'available_tags': Tag.objects.all(),
               'available_spaces': Space.objects.all(),
               }
    if request.method == 'POST':
        redirect_path = request.META.get('HTTP_REFERER')
        if request.POST.get('form_name') == 'tag-search-form':
            tag_name = request.POST.get('tag_name_to_be_searched')
            url = reverse('core:tags', kwargs={'tag_name': tag_name})
            return redirect(url)
        if request.POST.get("form_name") == "post-create-form":
            print("post-create-form received")
            post_model_handler.create_post(request=request)
        if request.POST.get("form_name") == "post-update-form":
            print("post-update-form received")
            post_model_handler.update_post(request=request)
        if request.POST.get("form_name") == "tag-create-form":
            print("tag-create-form received")
            is_tag_name_valid = tag_model_handler.validate_tag(request=request)
            if is_tag_name_valid:
                tag_model_handler.create_tag(request=request)
        print(request.POST)
        return HttpResponseRedirect(redirect_path)
    return render(request, "tags.html", context=context)


@login_required(login_url="core:signin")
def spaces(request, space_name):
    print(f"TAG NAME IS: {space_name}")
    # Get the Tag object for given tag name
    try:
        space = Space.objects.get(name=space_name)
    except Space.DoesNotExist:
        path = request.META.get('HTTP_REFERER')
        # TODO: Add does not exist message here
        return HttpResponseRedirect(path)
    # Get all posts with specific tag name
    posts = space.posts.all().order_by('-created')
    if request.method == 'POST':
        if request.POST.get('form_name') == 'tag-search-form':
            print(request.POST)
            tag_name = request.POST.get('tag_name_to_be_searched')
    # Create list of post owners
    post_owner_profile_list = list()
    for post in posts:
        user_obj = User.objects.get(username=post.owner_username)
        profile_obj = Profile.objects.get(user=user_obj)
        post_owner_profile_list.append(profile_obj)
    request_owner_user_object = User.objects.get(username=request.user.username)
    request_owner_user_profile = Profile.objects.get(user=request_owner_user_object)
    post_owner_profile_list_with_posts = zip(post_owner_profile_list, posts)
    context = {"post_owner_profile_list_with_posts": post_owner_profile_list_with_posts,
               "request_owner_user_profile": request_owner_user_profile,
               'available_tags': Tag.objects.all(),
               'available_spaces': Space.objects.all(),
               }
    if request.method == 'POST':
        redirect_path = request.META.get('HTTP_REFERER')
        if request.POST.get('form_name') == 'space-search-form':
            space_name = request.POST.get('space_name_to_be_searched')
            url = reverse('core:spaces', kwargs={'space_name': space_name})
            return redirect(url)
        if request.POST.get("form_name") == "post-create-form":
            print("post-create-form received")
            post_model_handler.create_post(request=request)
        if request.POST.get("form_name") == "post-update-form":
            print("post-update-form received")
            post_model_handler.update_post(request=request)
        if request.POST.get("form_name") == "space-create-form":
            print("space-create-form received")
            is_space_name_valid = space_model_handler.validate_space(request=request)
            if is_space_name_valid:
                space_model_handler.create_space(request=request)
        print(request.POST)
        return HttpResponseRedirect(redirect_path)
    return render(request, "spaces.html", context=context)


@login_required(login_url="core:signin")
def feed(request: object):
    # Get the profile owner user object and profile
    request_owner_user_object = User.objects.get(username=request.user.username)
    request_owner_user_profile = Profile.objects.get(user=request_owner_user_object)
    # Get all posts with specific tag name
    followings_username = list()
    # Get the posts in a list
    for followed in request_owner_user_profile.following:
        # following_profile = Profile.objects.get(id_user=followed)
        # following_profiles_posts = Post.objects.filter(owner_username=following_profile.user.username)
        # followings_posts.append(following_profiles_posts)
        following_profile = Profile.objects.get(id_user=followed)
        followings_username.append(following_profile.user.username)
        # print(type(following_profiles_posts))
    followings_posts = Post.objects.filter(owner_username__in=followings_username).order_by('-created')
    print(followings_username)
    followings_profiles = list()
    for post in followings_posts:
        post_owner_user_object = User.objects.get(username=post.owner_username)
        post_owner_profile_object = Profile.objects.get(user=post_owner_user_object)
        followings_profiles.append(post_owner_profile_object)
    print(followings_profiles)
    following_profile_list_with_posts = zip(followings_profiles, followings_posts)
    context = {'following_profile_list_with_posts': following_profile_list_with_posts,
               "request_owner_user_profile": request_owner_user_profile,
               'available_tags': Tag.objects.all(),
               'available_spaces': Space.objects.all(),
               }
    if request.method == 'POST':
        redirect_path = request.META.get('HTTP_REFERER')
        if request.POST.get("form_name") == "post-create-form":
            print("post-create-form received")
            post_model_handler.create_post(request=request)
        if request.POST.get("form_name") == "post-update-form":
            print("post-update-form received")
            post_model_handler.update_post(request=request)
        if request.POST.get("form_name") == "space-create-form":
            print("space-create-form received")
            is_space_name_valid = space_model_handler.validate_space(request=request)
            if is_space_name_valid:
                space_model_handler.create_space(request=request)
        if request.POST.get("form_name") == "tag-create-form":
            print("tag-create-form received")
            is_tag_name_valid = tag_model_handler.validate_tag(request=request)
            if is_tag_name_valid:
                tag_model_handler.create_tag(request=request)
        print(request.POST)
        return HttpResponseRedirect(redirect_path)
    return render(request, "feed.html", context=context)
