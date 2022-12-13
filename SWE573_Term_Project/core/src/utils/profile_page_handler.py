from django.http import HttpResponseRedirect
from ...models import Profile, Post
from django.shortcuts import render
from . import post_model_handler

def profile_page_handler_main(request):
    print("Profile handler is called")
    if request.method == "POST":
        return profile_post_method_handler(request=request)
    elif request.method == "GET":
        return profile_get_method_handler(request=request)
    else:
        raise "Invalid HTTP Method"

def profile_post_method_handler(request):
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

def profile_get_method_handler(request):
    # TODO - Dağlar: Do I need to change this function to dynamically rendering another page
    user_profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(owner_username=request.user.username).order_by('-created_at')
    return render(request, "profile.html", {'user_profile': user_profile, 'posts': posts, })



