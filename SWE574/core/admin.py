from django.contrib import admin
from .models import Profile, Post, Tag, Space, Comment


# Models to be displayed within admin panel

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Space)
# admin.site.register(Badge)
admin.site.register(Comment)
