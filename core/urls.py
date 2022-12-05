from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.feed, name="feed"),
    path("feed", views.feed, name="feed"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("logout", views.logout, name="logout"),
    path("settings", views.settings, name="settings"),
    path("delete_account", views.delete_account, name="delete_account")
    # path("feed", views.feed, name="logout"),
    # path("profile", views.profile, name="logout"),
]