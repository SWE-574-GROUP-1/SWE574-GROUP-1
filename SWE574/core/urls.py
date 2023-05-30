from django.urls import path
from . import views
from .src.controllers import annotation_controller
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
    path("about/", views.about, name="about"),
    path("delete_account", views.delete_account, name="delete_account"),
    path("delete_post", views.delete_post, name="delete_post"),
    path("preview/", generate_preview.generate_preview, name="generate"),
    path("search", views.search, name="search"),
    path("follow", views.follow, name="follow"),
    path("join", views.join, name="join"),
    path("tags", views.tags_index, name="tags_index"),
    path("tags/wiki-data-search", views.tag_wiki_data_search, name="tag_wiki_data_search"),
    path("tags/search", views.tags_search, name="tags_search"),
    path("tags/all", views.all_tags, name="all_tags"),
    path("tags/<str:tag_name>", views.tag_posts, name="tag_posts"),
    path("spaces", views.spaces_index, name="spaces_index"),
    path("spaces/search", views.spaces_search, name="spaces_search"),
    path("spaces/create", views.create_space, name="create_space"),
    path("spaces/all", views.all_spaces, name="all_spaces"),
    path("spaces/<str:space_name>", views.space_posts, name="space_posts"),
    path("post/detail/<str:post_id>", views.post_detail, name="post_detail"),
    path("post/create", views.create_post, name="create_post"),
    path("post/update", views.update_post, name="update_post"),
    path("post/like/<str:post_id>", views.like_post, name="like_post"),
    path("post/dislike/<str:post_id>", views.dislike_post, name="like_post"),
    path("post/bookmark_post", views.bookmark_post, name="bookmark_post"),
    path("fetch-og-tags", views.fetch_og_tags, name="fetch_og_tags"),
    path("annotations/create", annotation_controller.create_annotation, name="create_annotation"),
    path("annotations/search", annotation_controller.get_annotations, name="get_annotations"),
    path("badges", views.badges, name="badges"),
    path('add-comment/<uuid:post_id>/', views.add_comment, name='add_comment'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path("following_list", views.following_list, name="following_list"),
    path("follower_list", views.follower_list, name="follower_list"),
]
