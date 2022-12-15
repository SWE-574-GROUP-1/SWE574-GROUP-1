from django.contrib.auth.decorators import login_required
from .src.pages.profile_page_handler import profile_page_handler_main
from .src.models.post_model_handler import __delete_post__, __book_post__
from .src.pages.signup_page_handler import signup_page_handler_main
from .src.pages.signin_page_handler import signin_page_handler_main
from .src.models.user_model_handler import *
from .src.pages.settings_page_handler import settings_page_handler_main
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
def profile(request):
    return profile_page_handler_main(request=request)


