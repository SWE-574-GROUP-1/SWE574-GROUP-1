from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    uid = models.IntegerField()
    bio = models.TextField(blank=True)
    # Tells django where to upload, if folder does not exist then django creates it
    profile_image = models.ImageField(upload_to="profile_images", default="blank-profile-picture.png")
    location: models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.username