import random
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from .models import Profile, Tag, Space, Post, User
from .src.models import post_model_handler, tag_model_handler, space_model_handler
from .src.models.post_model_handler import __delete_post__, __book_post__
from .src.models.user_model_handler import delete_user
from .src.pages.profile_page_handler import profile_page_handler_main
from .src.pages.settings_page_handler import settings_page_handler_main
from .src.pages.signin_page_handler import signin_page_handler_main
from .src.pages.signup_page_handler import signup_page_handler_main
import json


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
    # Sign-out the user
    auth.logout(request)
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
            context["search_result_user_profiles"] = search_result_user_profiles

            tag_results = Tag.objects.filter(name__icontains=keyword)
            context["tag_results"] = tag_results

            post_results = Post.objects.filter(Q(link__icontains=keyword) | Q(caption__icontains=keyword))
            context["post_results"] = post_results

            space_results = Space.objects.filter(name__icontains=keyword)
            context["space_results"] = space_results
    return render(request, "search.html", context=context)


@login_required(login_url="core:signin")
def follow(request):
    logged_in_user = User.objects.get(username=request.user.username)
    user_to_be_followed = User.objects.get(id=request.GET.get('profile_owner_user_id'))

    if logged_in_user.profile in user_to_be_followed.profile.followers.all():
        """ remove from array field followers """
        user_to_be_followed.profile.followers.remove(logged_in_user.profile)
        followed = False
    else:
        # save changes
        user_to_be_followed.profile.followers.add(logged_in_user.profile)
        followed = True

    user_to_be_followed.profile.save()
    logged_in_user.profile.save()
    print(f"{user_to_be_followed.profile.followers.count()=}")
    followers_count = user_to_be_followed.profile.followers.count()
    following_count = user_to_be_followed.profile.following.count()

    return JsonResponse({'followed': followed, 'followers_count': followers_count, 'following_count': following_count})


def tags_search(request):
    tag_name = request.POST.get('tag_name_to_be_searched')
    # return posts where has tags like tag_name
    tags = Tag.objects.filter(name__icontains=tag_name)
    posts = Post.objects.filter(tags__in=tags).distinct().prefetch_related(
        Prefetch('tags', queryset=tags, to_attr='matching_tags'))

    tag_cloud = get_tag_cloud()

    return render(request, 'tags.html', {'posts': posts, 'tag_name': tag_name, 'tag_cloud': tag_cloud})


def tags_index(request):
    tag_cloud = get_tag_cloud()
    return render(request, 'tags.html', {'tag_cloud': tag_cloud})


def tag_posts(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    posts = Post.objects.filter(tags=tag).prefetch_related('tags')
    tag_cloud = get_tag_cloud()
    return render(request, 'tags.html', {'posts': posts, 'tag_name': tag_name, 'tag_cloud': tag_cloud})


def get_tag_cloud():
    tags = Tag.objects.annotate(count=Count('posts')).order_by('-count')
    max_count = tags[0].count if tags else 0
    min_count = tags[len(tags) - 1].count if tags else 0
    range_count = max_count - min_count
    font_min = 12
    font_max = 36
    font_range = font_max - font_min
    for tag in tags:
        tag.font_size = font_min + (font_range * (tag.count - min_count) / (range_count or 1))

    # randomize tag order
    tags = sorted(tags, key=lambda x: random.random())

    return tags


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
            # TODO: Is this line required? --> tag_name = request.POST.get('tag_name_to_be_searched')
    # Create list of post owners
    post_owner_profile_list = list()
    for post in posts:
        user_obj = User.objects.get(username=post.owner.username)
        profile_obj = Profile.objects.get(user=user_obj)
        post_owner_profile_list.append(profile_obj)
    request_owner_user_object = User.objects.get(
        username=request.user.username)
    request_owner_user_profile = Profile.objects.get(
        user=request_owner_user_object)
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


@login_required
def update_post(request):
    if request.method == 'POST':
        print("post-update-form received")
        post_model_handler.update_post(request=request)
    # redirect back
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def create_post(request):
    if request.method == 'POST':
        print("post-create-form received")
        post_model_handler.create_post(request=request)
    # redirect back
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="core:signin")
def feed(request: object):
    # Get the profile owner user object and profile
    request_owner_user_object = User.objects.get(username=request.user.username)
    # Get all posts with specific tag name
    followings_user = list()
    # Get the posts in a list
    for following_profile in request_owner_user_object.profile.following.all():
        followings_user.append(following_profile.user)
    followings_posts = Post.objects.filter(owner__in=followings_user).order_by('-modified')
    followings_profiles = list()
    for post in followings_posts:
        post_owner_user_object = User.objects.get(username=post.owner.username)
        post_owner_profile_object = Profile.objects.get(
            user=post_owner_user_object)
        followings_profiles.append(post_owner_profile_object)
    following_profile_list_with_posts = zip(
        followings_profiles, followings_posts)
    context = {
        'following_profile_list_with_posts': following_profile_list_with_posts,
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
            is_space_name_valid = space_model_handler.validate_space(
                request=request)
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


@login_required(login_url="core:signin")
def post_detail(request, post_id):
    post = Post.objects.get(post_id=post_id)
    request_owner_user_profile = Profile.objects.get(user=request.user)
    return render(
        request, "post_detail.html",
        {"post": post, "request_owner_user_profile": request_owner_user_profile}
    )


@login_required(login_url="core:signin")
def like_post(request, post_id):
    post = Post.objects.get(post_id=post_id)
    user = User.objects.get(username=request.user.username)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    return JsonResponse({'liked': liked, 'count': post.total_likes()})


@login_required(login_url="core:signin")
def dislike_post(request, post_id):
    post = Post.objects.get(post_id=post_id)
    user = User.objects.get(username=request.user.username)

    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(user)
        disliked = False
    else:
        post.dislikes.add(user)
        disliked = True

    return JsonResponse({'disliked': disliked, 'count': post.total_dislikes()})


@login_required(login_url="core:signin")
def bookmark_post(request, post_id):
    post = Post.objects.get(post_id=post_id)
    user = User.objects.get(username=request.user.username)

    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(user)
        bookmarked = False
    else:
        post.bookmarks.add(user)
        bookmarked = True

    return JsonResponse({'bookmarked': bookmarked})


# this methods fetch the given url's og tags and return json response as img, title, description


@login_required(login_url="core:signin")
def fetch_og_tags(request):

    """ get url from request body, post request """
    data = json.loads(request.body.decode("utf-8"))
    url = data["url"]
    # print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    og_image = soup.find('meta', property='og:image')
    og_title = soup.find('meta', property='og:title')
    og_description = soup.find('meta', property='og:description')
    # print(og_image['content'])
    # print(og_title['content'])
    # print(og_description['content'])
    return JsonResponse({'img': og_image['content'], 'title': og_title['content'],
                         'description': og_description['content']})


def all_tags(request):
    tags = Tag.objects.all()
    return JsonResponse({'tags': list(tags.values())})


def tag_wiki_data_search(request):
    tag_name = request.GET.get('search', 'python')
    url = "https://www.wikidata.org"
    url += f"{url}/w/api.php?action=wbsearchentities&format=json&search={tag_name}&language=tr&type=item"
    response = requests.get(url)

    if len(response.json()['search']) > 1:
        response = map(lambda x: {'id': x['id'], 'name': x['label'], 'description': x['description']},
                       response.json()['search'])
        response = list(response)
    else:
        response = list()

    return JsonResponse(response, safe=False)


# For badge page and model added

@login_required(login_url="core:signin")
def badges(request):
    return render(
        request, "badges.html"
    )
