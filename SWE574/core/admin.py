from django.contrib import admin
from .models import Profile, Post, Tag, Space, Comment, Bookmark


# Models to be displayed within admin panel

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Space)
admin.site.register(Bookmark)
admin.site.register(Comment)
