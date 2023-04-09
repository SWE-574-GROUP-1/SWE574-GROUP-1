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
    path('about2/', views.about2, name='about2'),
    path('profile/<str:profile_owner_username>/about/', views.about, name='about'),
    path("tags", views.tags_index, name="tags_index"),
    path("tags/search", views.tags_search, name="tags_search"),
    path("tags/all", views.all_tags, name="all_tags"),
    path("tags/<str:tag_name>", views.tag_posts, name="tag_posts"),
    path("spaces/<str:space_name>", views.spaces, name="spaces"),
    path("post/detail/<str:post_id>", views.post_detail, name="post_detail"),
    path("post/create", views.create_post, name="create_post"),
    path("post/update", views.update_post, name="update_post"),
    path("post/like/<str:post_id>", views.like_post, name="like_post"),
    path("post/dislike/<str:post_id>", views.dislike_post, name="like_post"),
    path("post/bookmark/<str:post_id>", views.bookmark_post, name="bookmark_post"),
    path("fetch-og-tags", views.fetch_og_tags, name="fetch_og_tags"),
    # path("feed", views.feed, name="logout"),
    # path("profile", views.profile, name="logout"),
]
