"""Contains utility methods for Profile model"""
from ...models import Profile
from django.contrib.auth.models import User


def create_profile(request: object) -> None:
    """
    Implementation of creating a Profile model.
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: None
    """
    username = request.POST.get("username")
    # Create profile object for the new user
    user_model = User.objects.get(username=username)
    new_profile = Profile.objects.create(user=user_model)
    new_profile.available_labels.append('default')
    new_profile.save()
