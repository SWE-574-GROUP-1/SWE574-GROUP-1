from django.contrib import admin
from .models import Profile, Post, Tag


# Models to be displayed within admin panel

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Tag)
