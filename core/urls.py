from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("logout", views.logout, name="logout"),
    # path("feed", views.feed, name="logout"),
    # path("profile", views.profile, name="logout"),
]