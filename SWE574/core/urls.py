from django.urls import path
from . import views
from .src.utils import generate_preview

app_name = "core"

urlpatterns = [
    path("", views.feed, name="feed"),
    path("feed", views.feed, name="preview"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("logout", views.logout, name="logout"),
    path("settings", views.settings, name="settings"),
    path("profile/<str:profile_owner_username>/", views.profile, name="profile"),
    path("delete_account", views.delete_account, name="delete_account"),
    path("delete_post", views.delete_post, name="delete_post"),
    path("book_post", views.book_post, name="book_post"),
    path("preview/", generate_preview.generate_preview, name="generate"),
    path("search", views.search, name="search"),
    path("follow", views.follow, name="follow"),
    path("tags/<str:tag_name>", views.tags, name="tags"),
    path("spaces/<str:space_name>", views.spaces, name="spaces")
    # path("feed", views.feed, name="logout"),
    # path("profile", views.profile, name="logout"),
]
