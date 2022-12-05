from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from datetime import datetime
from uuid import uuid4
# Create your models here.

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    id_user = models.IntegerField(unique=True)
    bio = models.TextField(default="Write something here")
    profile_image = models.ImageField(upload_to="profile_images", default="profile_images/blank-profile-picture.png")
    
    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    # Fields that are automatically filled
    post_id = models.UUIDField(primary_key=True, default=uuid4, unique=True)
    owner_username = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)
    # Fields that are filled by owner user
    link = models.URLField(blank=False)  # URLField cannot be empty, this not twitter :) 
    caption = models.TextField(blank=True)  # Captio can be empty
    # Fields that are filled by other users
    # TODO: Learn more about posting a link, and having a preview in python
    # TODO: Learn more about using a foreign key as attribute
    bookmarked_by = ArrayField(models.IntegerField(), default=list, blank=True,)
    # bookmarked_by = models.ForeignKey(Profile.id_user, on_delete=models.CASCADE)
    num_of_bookmarks = models.IntegerField(default=0)

    def __str__(self):
        return self.owner_username