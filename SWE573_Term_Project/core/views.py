from django.contrib.auth.decorators import login_required
from .src.utils.profile_page_handler import profile_page_handler_main
from .src.utils.post_model_handler import __delete_post__, __book_post__
from .src.utils.signup_page_handler import signup_page_handler_main
from .src.utils.signin_page_handler import signin_page_handler_main
from .src.utils.user_model_handler import *
from .src.utils.settings_page_handler import settings_page_handler_main

@login_required(login_url="core:signin")
def feed(request):
    return render(request, 'test.html')


def signup(request):
    return signup_page_handler_main(request=request)


def signin(request):
    return signin_page_handler_main(request=request)


@login_required(login_url='core:signin')
def settings(request):
    return settings_page_handler_main(request=request)


@login_required(login_url="core:signin")
def logout(request):
    auth.logout(request)
    # TODO - Dağlar: Change this to homepage when created
    return redirect("core:signin")

    
@login_required(login_url="core:signin")
def delete_account(request):
    return delete_user(request=request)


@login_required(login_url='core:signin')
def delete_post(request):
    return __delete_post__(request=request)


@login_required(login_url='core:signin')
def book_post(request):
    return __book_post__(request=request)


@login_required(login_url="core:signin")
def profile(request):
    return profile_page_handler_main(request=request)


