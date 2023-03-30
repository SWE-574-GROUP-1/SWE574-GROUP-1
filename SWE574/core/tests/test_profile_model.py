import os
from unittest import TestCase
from ..models import *
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageFieldFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ObjectDoesNotExist

username = "test_username"
email = "test@test.com"
password = "test_password"


class ProfileTestCase(TestCase):
    """Unit tests for Profile model"""

    def setUp(self) -> None:
        """Initialize objects"""
        self.user = User.objects.create_user(username=username, email=email, password=password)
        self.profile = Profile.objects.create(user=self.user)

    def tearDown(self) -> None:
        """Delete objects from db after tests"""
        self.profile.delete()

    def test_delete_profile(self):
        """Assert that after deleting the profile, 0 profile remains"""
        profile = Profile.objects.get(user=self.user)
        profile.delete()
        profile_count = Profile.objects.count()
        self.assertEqual(profile_count, 0)

    def test_delete_profile_user(self):
        """Assert that user is deleted when profile is deleted"""
        profile = Profile.objects.get(user=self.user)
        profile.delete()
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username=username)

    def test_delete_profile_user_count(self):
        """Assert that user count is 0 when profile is deleted"""
        profile = Profile.objects.get(user=self.user)
        profile.delete()
        user_count = User.objects.count()
        self.assertEqual(user_count, 0)

    def test_delete_user(self):
        """Assert that after deleting the user, 0 user remains"""
        user = User.objects.get(username=username)
        user.delete()
        user_count = User.objects.count()
        self.assertEqual(user_count, 0)

    def test_delete_user_profile(self):
        """Assert that profile is deleted when user is deleted"""
        user = User.objects.get(username=username)
        user.delete()
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(id=self.user.id)

    def test_delete_user_profile_count(self):
        """Assert that profile count is 0, when user is deleted"""
        user = User.objects.get(username=username)
        user.delete()
        profile_count = Profile.objects.count()
        self.assertEqual(profile_count, 0)

    def test_user_creation(self):
        """Assert that user is created at setUp"""
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_profile_creation(self):
        """Assert that profile is created at setup"""
        profile_count = Profile.objects.count()
        self.assertEqual(profile_count, 1)

    def test_profile_user_relation(self):
        """Test that the user field is a OneToOne to the User model"""
        user = self.profile.user
        _user = User.objects.get(username=username)
        self.assertEqual(user, _user)

    def test_profile_bio_default(self):
        """Test that bio field is default 'Write something here'"""
        profile = self.profile
        default = 'Write something here'
        bio = profile.bio
        self.assertEqual(bio, default)

    def test_profile_bio_max_length(self):
        """Test that the bio field is limited to 100 characters."""
        profile = self.profile
        max_length = profile._meta.get_field('bio').max_length
        self.assertEqual(max_length, 100)

    def test_profile_bio_dtype(self):
        """Test that dtype of bio field is str"""
        profile = self.profile
        self.assertTrue(isinstance(profile.bio, str))

    def test_profile_bio_can_be_updated(self):
        """Assert that bio can be updated"""
        profile = self.profile
        new_bio = "This is new bio!"
        profile.bio = new_bio
        profile.save()
        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.bio, new_bio)

    def test_profile_image_default(self):
        """Assert default profile image is 'profile_images/blank-profile-picture.png'"""
        profile_img = self.profile.profile_image
        default = 'profile_images/blank-profile-picture.png'
        self.assertEqual(profile_img.name, default)

    def test_profile_image_dtype(self):
        """Assert that default dtype of profile images is ImageFieldFile"""
        profile_img = self.profile.profile_image
        self.assertTrue(isinstance(profile_img, ImageFieldFile))

    def test_profile_image_path(self):
        """Assert that profile image is in /app/images/profile_images/ directory"""
        profile_img_path = self.profile.profile_image.path
        default_dir = '/app/images/profile_images/'
        self.assertTrue(default_dir in profile_img_path)

    def test_profile_image_can_be_updated(self):
        """Assert that profile image can be updated"""
        new_image = SimpleUploadedFile("new_image.jpg", b"new image content")
        self.profile.profile_image = new_image
        self.profile.save()
        self.assertTrue(new_image.name in self.profile.profile_image.path)
        os.remove(self.profile.profile_image.path)

    def test_profile_image_updated_dtype(self):
        """Assert that dtype of updated profile image is ImageFieldFile"""
        new_image = SimpleUploadedFile("new_image.jpg", b"new image content")
        self.profile.profile_image = new_image
        self.profile.save()
        self.assertTrue(isinstance(self.profile.profile_image, ImageFieldFile))
        os.remove(self.profile.profile_image.path)

    def test_profile_image_updated_dir(self):
        """Assert that dir of updated profile image is true"""
        new_image = SimpleUploadedFile("new_image.jpg", b"new image content")
        self.profile.profile_image = new_image
        self.profile.save()
        default_dir = '/app/images/profile_images/'
        self.assertTrue(default_dir in self.profile.profile_image.path)
        os.remove(self.profile.profile_image.path)

    def test_background_image_default(self):
        """Assert default background image is 'background_images/bg-image-5.jpg'"""
        bg_img = self.profile.background_image
        default = 'background_images/bg-image-5.jpg'
        self.assertEqual(bg_img, default)

    def test_background_image_dtype(self):
        """Assert that default dtype of background images is ImageFieldFile"""
        bg_img = self.profile.background_image
        self.assertTrue(isinstance(bg_img, ImageFieldFile))

    def test_background_image_can_be_updated(self):
        """Assert that background image can be updated"""
        new_img_path = '/app/images/background_images/bg-image-3.jpg'
        self.profile.background_image = new_img_path
        self.profile.save()
        self.assertEqual(new_img_path, self.profile.background_image.path)

    def test_background_image_updated_dtype(self):
        """Assert that dtype of updated background image is ImageFieldFile"""
        new_img_path = '/app/images/background_images/bg-image-3.jpg'
        self.profile.background_image = new_img_path
        self.profile.save()
        self.assertTrue(isinstance(self.profile.background_image, ImageFieldFile))

    def test_background_image_updated_dir(self):
        """Assert that dir of updated background image is true"""
        new_img_path = '/app/images/background_images/bg-image-3.jpg'
        self.profile.background_image = new_img_path
        self.profile.save()
        default_dir = '/app/images/profile_images/'
        self.assertTrue(default_dir in self.profile.profile_image.path)

    def test_followers_default(self):
        """Assert that followers field is empty list by default"""
        followers = self.profile.followers
        self.assertEqual(followers, list())

    def test_followers_dtype(self):
        """Assert that followers dtype is list"""
        followers = self.profile.followers
        self.assertTrue(isinstance(followers, list))

    def test_following_default(self):
        """Assert that following field is empty list by default"""
        following = self.profile.following
        self.assertEqual(following, list())

    def test_following_dtype(self):
        """Assert that following dtype is list"""
        following = self.profile.following
        self.assertTrue(isinstance(following, list))
