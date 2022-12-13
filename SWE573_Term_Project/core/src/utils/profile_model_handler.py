from ...models import Profile
from django.contrib.auth.models import User


def create_profile(request):
    username = request.POST.get("username")
    # Create profile object for the new user
    user_model = User.objects.get(username=username)
    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
    new_profile.save()
    pass