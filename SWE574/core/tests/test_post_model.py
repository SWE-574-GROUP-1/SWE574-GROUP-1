import uuid
from unittest import TestCase
from ..models import Post, User, Tag, Space
from django.db import models
from model_utils.models import TimeStampedModel

username = "test_user"
email = "test@test.com"
password = "test_password"
link = "https://docs.djangoproject.com/en/4.1/topics/testing/overview/"


class TestPost(TestCase):
    """Unit tests for Post model"""

    def setUp(self):
        """Initialize objects"""
        self.user = User.objects.create_user(username=username, email=email, password=password)
        self.post = Post.objects.create(owner=self.user, link=link)

    def tearDown(self) -> None:
        """Delete objects from db after tests"""
        self.user.delete()

    def test_post_setup(self):
        """Assert that setup is correct"""
        test_post = Post.objects.get(owner=self.user)
        self.assertEqual(test_post.link, link)
        self.assertEqual(test_post.owner.username, username)
        self.assertEqual(test_post.owner.email, email)

    def test_post_invalid_attr(self):
        """Assert that accessing invalid field raise an AttributeError"""
        with self.assertRaises(AttributeError):
            self.post.invalid_field_1
            self.post.invalid_field_2
            self.post.invalid_field_3

    # # Test Deleting Model
    def test_post_delete(self):
        """Assert that deleting post works"""
        self.post.delete()
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(owner=self.user)
        count = Post.objects.count()
        self.assertEqual(0, count)

    def test_post_dtype(self):
        self.assertIsInstance(self.post, TimeStampedModel)
        self.assertIsInstance(self.post, models.Model)

    def test_post_user(self):
        """Assert that OneToMany relation in between user and post"""
        test_post = Post.objects.get(owner=self.user)
        self.assertEqual(test_post.owner.id, self.post.owner.id)
        self.assertEqual(test_post.owner.username, self.post.owner.username)
        self.assertEqual(test_post.owner.email, self.post.owner.email)

    def test_user_deletes_posts(self):
        """Assert that deleting the user deletes all posts"""
        user = User.objects.get(username=username)
        user.delete()
        count = Post.objects.count()
        self.assertEqual(count, 0)

    def test_post_change_username(self):
        """Assert changing user.username does not affect accessing post"""
        # Change the username
        new_username = "test_change_username"
        self.user.username = new_username
        self.user.save()
        # Get the changed version
        test_post = Post.objects.get(owner=self.user)
        self.assertEqual(test_post.owner.username, self.user.username)

    def test_post_not_delete_user(self):
        """Assert that deleting post does not delete user"""
        test_post = Post.objects.get(owner=self.user)
        test_post.delete()
        count = User.objects.count()
        self.assertEqual(1, count)

    def test_post_id_dtype(self):
        """Assert that dtype of post_id is UUID"""
        self.assertIsInstance(self.post.post_id, uuid.UUID)

    def test_post_id_cannot_update(self):
        """Assert that post_id cannot be updated"""
        # Get the original version
        initial_id = self.post.post_id
        # Update post_id
        new_id = uuid.uuid4()
        test_post = Post.objects.get(post_id=initial_id)
        test_post.post_id = new_id
        test_post.save()
        # Get the updated version
        test_post = Post.objects.get(owner=self.user)
        self.assertNotEqual(new_id, initial_id)
        self.assertEqual(initial_id, test_post.post_id)
        self.assertNotEqual(new_id, test_post.post_id)
        self.assertEqual(self.post.post_id, test_post.post_id)

    def test_post_can_be_liked(self):
        """Assert that post can be liked"""
        other_user = User.objects.create_user(
            username="other" + username, email="other" + email, password=password
        )
        self.post.likes.add(other_user)
        count = self.post.likes.count()
        self.assertEqual(count, 1)
        other_user.delete()

    def test_post_liked_dtype(self):
        """Assert that post can be liked by user dtype"""
        other_user = User.objects.create_user(
            username="other" + username, email="other" + email, password=password
        )
        self.post.likes.add(other_user)
        user_obj = self.post.likes.get(username=other_user.username)
        self.assertIsInstance(user_obj, User)
        other_user.delete()

    def test_post_can_be_unliked(self):
        """Assert that post can be unliked"""
        other_user = User.objects.create_user(
            username="other" + username, email="other" + email, password=password
        )
        self.post.likes.add(other_user)
        count = self.post.likes.count()
        self.assertEqual(count, 1)
        self.post.likes.remove(other_user)
        count = self.post.likes.count()
        self.assertEqual(count, 0)
        other_user.delete()

    def test_post_can_have_multiple_likes(self):
        """Assert that post can have more than 1 like"""
        other_user = User.objects.create_user(
            username="other" + username, email="other_" + email, password=password
        )
        other_user2 = User.objects.create_user(
            username="other2" + username, email="other2" + email, password=password
        )
        self.post.likes.add(other_user, other_user2)
        count = self.post.likes.count()
        self.assertEqual(count, 2)
        other_user.delete()
        other_user2.delete()

    def test_post_like_decrease_ondelete(self):
        """Assert that deleting user removes the like"""
        other_user = User.objects.create_user(
            username="other" + username, email="other_" + email, password=password
        )
        other_user2 = User.objects.create_user(
            username="other2" + username, email="other2" + email, password=password
        )
        self.post.likes.add(other_user, other_user2)
        other_user.delete()
        count = self.post.likes.count()
        self.assertEqual(count, 1)
        other_user2.delete()
        count = self.post.likes.count()
        self.assertEqual(count, 0)

    def test_post_disliked_dtype(self):
        """Assert that dislike dtype is correct"""
        other_user = User.objects.create_user(
            username="other" + username, email="other" + email, password=password
        )
        self.post.dislikes.add(other_user)
        user_obj = self.post.dislikes.get(username=other_user.username)
        self.assertIsInstance(user_obj, User)
        other_user.delete()

    def test_post_can_be_disliked(self):
        """Assert that post can be disliked"""
        other_user = User.objects.create_user(
            username="other" + username, email="other_" + email, password=password
        )
        self.post.dislikes.add(other_user)
        count = self.post.dislikes.count()
        self.assertEqual(count, 1)
        other_user.delete()

    def test_post_can_be_undisliked(self):
        """Assert that post can be undisliked"""
        other_user = User.objects.create_user(
            username="other" + username, email="other" + email, password=password
        )
        self.post.dislikes.add(other_user)
        count = self.post.dislikes.count()
        self.assertEqual(count, 1)
        self.post.dislikes.remove(other_user)
        count = self.post.dislikes.count()
        self.assertEqual(count, 0)
        other_user.delete()

    def test_post_can_have_multiple_dislikes(self):
        """Assert that post can have more than 1 dislike"""
        other_user = User.objects.create_user(
            username="other" + username, email="other_" + email, password=password
        )
        other_user2 = User.objects.create_user(
            username="other2" + username, email="other2" + email, password=password
        )
        self.post.dislikes.add(other_user)
        self.post.dislikes.add(other_user2)
        count = self.post.dislikes.count()
        self.assertEqual(count, 2)
        other_user.delete()
        other_user2.delete()

    def test_post_dislike_decrease_ondelete(self):
        """Assert that deleting user removes the dislike"""
        other_user = User.objects.create_user(
            username="other" + username, email="other_" + email, password=password
        )
        other_user2 = User.objects.create_user(
            username="other2" + username, email="other2" + email, password=password
        )
        self.post.dislikes.add(other_user, other_user2)
        other_user.delete()
        count = self.post.dislikes.count()
        self.assertEqual(count, 1)
        other_user2.delete()
        count = self.post.dislikes.count()
        self.assertEqual(count, 0)

    def test_post_can_be_bookmarked(self):
        """Assert that post can be bookmarked"""
        other_user = User.objects.create_user(
            username="other" + username, email="other_" + email, password=password
        )
        self.post.bookmarks.add(other_user)
        count = self.post.bookmarks.count()
        self.assertEqual(count, 1)
        other_user.delete()

    def test_post_bookmark_dtype(self):
        """Assert that post can be liked by user dtype"""
        other_user = User.objects.create_user(
            username="other" + username, email="other" + email, password=password
        )
        self.post.bookmarks.add(other_user)
        user_obj = self.post.bookmarks.get(username=other_user.username)
        self.assertIsInstance(user_obj, User)
        other_user.delete()

    def test_post_can_be_unbookmarked(self):
        """Assert that post can be unbookmarked"""
        other_user = User.objects.create_user(
            username="other" + username, email="other" + email, password=password
        )
        self.post.bookmarks.add(other_user)
        count = self.post.bookmarks.count()
        self.assertEqual(count, 1)
        self.post.bookmarks.remove(other_user)
        count = self.post.bookmarks.count()
        self.assertEqual(count, 0)
        other_user.delete()

    def test_post_can_have_multiple_bookmarks(self):
        """Assert that post can have more than 1 bookmarked"""
        other_user = User.objects.create_user(
            username="other" + username, email="other_" + email, password=password
        )
        other_user2 = User.objects.create_user(
            username="other2" + username, email="other2" + email, password=password
        )
        self.post.bookmarks.add(other_user)
        self.post.bookmarks.add(other_user2)
        self.post.save()
        count = self.post.bookmarks.count()
        self.assertEqual(count, 2)
        other_user.delete()
        other_user2.delete()

    def test_post_bookmarks_decrease_ondelete(self):
        """Assert that deleting user removes the bookmarks"""
        other_user = User.objects.create_user(
            username="other" + username, email="other_" + email, password=password
        )
        other_user2 = User.objects.create_user(
            username="other2" + username, email="other2" + email, password=password
        )
        self.post.bookmarks.add(other_user, other_user2)
        other_user.delete()
        count = self.post.bookmarks.count()
        self.assertEqual(count, 1)
        other_user2.delete()
        count = self.post.bookmarks.count()
        self.assertEqual(count, 0)

    def test_post_owner_dtype(self):
        """Assert that dtype of owner field is User"""
        self.assertIsInstance(self.post.owner, User)

    def test_post_owner_cannot_update(self):
        """Assert that post ownership cannot be updated"""
        """Assert that post_id cannot be updated"""
        # Get the original version
        initial_owner = self.post.owner
        # Update post_id
        new_owner = User.objects.create_user(
            username="other" + username, email="other_" + email, password=password
        )
        test_post = Post.objects.get(owner=initial_owner)
        test_post.owner = new_owner
        test_post.save()
        # Get the updated version
        test_post = Post.objects.get(owner=initial_owner)
        self.assertNotEqual(initial_owner, new_owner)
        self.assertEqual(initial_owner.username, test_post.owner.username)
        self.assertNotEqual(new_owner.username, test_post.owner.username)
        self.assertEqual(self.post.owner.username, test_post.owner.username)
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(owner=new_owner)
        new_owner.delete()

    def test_link_dtype(self):
        """Assert that dtype of link is correct"""
        self.assertIsInstance(self.post.link, str)

    def test_link_can_updated(self):
        """Assert that link can be updated"""
        new_link = "https://www.youtube.com/watch?v=dV5j0lnHVTA"
        self.post.link = new_link
        self.post.save()
        updated_post = Post.objects.get(owner=self.user)
        self.assertEqual(updated_post.link, new_link)

    def test_link_cannot_empty(self):
        """Assert that link cannot be empty"""
        old_link = self.post.link
        new_link = ""
        self.post.link = new_link
        self.post.save()
        updated_post = Post.objects.get(owner=self.user)
        self.assertNotEqual(updated_post.link, new_link)
        self.assertEqual(updated_post.link, old_link)

    def test_caption_dtype(self):
        """Assert that dtype of caption is correct"""
        self.assertIsInstance(self.post.link, str)

    def test_caption_can_updated(self):
        """Assert that caption can be updated"""
        new_caption = "This is new caption!"
        self.post.caption = new_caption
        self.post.save()
        updated_post = Post.objects.get(owner=self.user)
        self.assertEqual(updated_post.caption, new_caption)

    def test_title_dtype(self):
        """Assert that dtype of title is correct"""
        self.assertIsInstance(self.post.title, str)

    def test_title_can_updated(self):
        """Assert that title can be updated"""
        new_title = "This is new title!"
        self.post.title = new_title
        self.post.save()
        updated_post = Post.objects.get(owner=self.user)
        self.assertEqual(updated_post.title, new_title)

    def test_title_max_length(self):
        """Assert that max length of title is 100"""
        max_length = self.post._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_description_dtype(self):
        """Assert that dtype of description is correct"""
        self.assertIsInstance(self.post.description, str)

    def test_description_can_updated(self):
        """Assert that description can be updated"""
        new_desc = "This is new description!"
        self.post.description = new_desc
        self.post.save()
        updated_post = Post.objects.get(owner=self.user)
        self.assertEqual(updated_post.description, new_desc)

    def test_description_max_length(self):
        """Assert that max length of description is 500"""
        max_length = self.post._meta.get_field('description').max_length
        self.assertEqual(max_length, 500)

    def test_preview_image_dtype(self):
        """Assert that dtype of preview_image is correct"""
        self.assertIsInstance(self.post.preview_image, str)

    def test_preview_image_can_updated(self):
        """Assert that preview_image can be updated"""
        new_preview_image = "This is new preview_image!"
        self.post.preview_image = new_preview_image
        self.post.save()
        updated_post = Post.objects.get(owner=self.user)
        self.assertEqual(updated_post.preview_image, new_preview_image)

    def test_preview_image_max_length(self):
        """Assert that max length of preview_image is 200"""
        max_length = self.post._meta.get_field('preview_image').max_length
        self.assertEqual(max_length, 200)

    def test_post_tags_dtype(self):
        """Assert that dtype of tags is Tag"""
        new_tag = Tag.objects.create(name="new_tag")
        self.post.tags.add(new_tag)
        self.post.save()
        updated_post_obj = Post.objects.get(owner=self.user)
        self.assertIsInstance(updated_post_obj.tags.get(name="new_tag"), Tag)
        new_tag.delete()

    def test_tag_can_be_removed(self):
        """Assert that tag can be removed form post"""
        new_tag = Tag.objects.create(name="new_tag1")
        self.post.tags.add(new_tag)
        self.post.save()
        updated_post_obj = Post.objects.get(owner=self.user)
        count = updated_post_obj.tags.count()
        self.assertEqual(count, 1)
        self.post.tags.remove(new_tag)
        count = updated_post_obj.tags.count()
        self.assertEqual(count, 0)
        new_tag.delete()

    def test_tag_delete(self):
        """Assert that deleting tag removes the tag from post"""
        new_tag = Tag.objects.create(name="new_tag")
        self.post.tags.add(new_tag)
        self.post.save()
        new_tag.delete()
        updated_post_obj = Post.objects.get(owner=self.user)
        count = updated_post_obj.tags.count()
        self.assertEqual(count, 0)
        with self.assertRaises(Tag.DoesNotExist):
            updated_post_obj.tags.get(name="new_tag")

    def test_post_can_have_multiple_tags(self):
        """Assert that post can have more than 1 tag"""
        new_tag1 = Tag.objects.create(name="new_tag1")
        new_tag2 = Tag.objects.create(name="new_tag2")
        self.post.tags.add(new_tag1)
        self.post.tags.add(new_tag2)
        self.post.save()
        updated_post_obj = Post.objects.get(owner=self.user)
        count = updated_post_obj.tags.count()
        self.assertEqual(count, 2)
        new_tag1.delete()
        new_tag2.delete()

    def test_reverse_call_tag_post(self):
        """Assert that post can be accessed from the tag"""
        new_tag1 = Tag.objects.create(name="new_tag")
        self.post.tags.add(new_tag1)
        self.post.save()
        post = new_tag1.posts.get(owner=self.user)
        self.assertEqual(post, self.post)
        new_tag1.delete()

    def test_post_space_dtype(self):
        """Assert that dtype of spaces is Space"""
        new_space = Space.objects.create(name="new_space")
        self.post.spaces.add(new_space)
        self.post.save()
        updated_post_obj = Post.objects.get(owner=self.user)
        self.assertIsInstance(updated_post_obj.spaces.get(name="new_space"), Space)
        new_space.delete()

    def test_space_can_be_removed(self):
        """Assert that space can be removed from post"""
        new_space = Space.objects.create(name="new_space")
        self.post.spaces.add(new_space)
        self.post.save()
        updated_post_obj = Post.objects.get(owner=self.user)
        count = updated_post_obj.spaces.count()
        self.assertEqual(count, 1)
        self.post.spaces.remove(new_space)
        count = updated_post_obj.spaces.count()
        self.assertEqual(count, 0)
        new_space.delete()

    def test_space_delete(self):
        """Assert that deleting space removes the space from post"""
        new_space = Space.objects.create(name="new_space")
        self.post.spaces.add(new_space)
        self.post.save()
        new_space.delete()
        updated_post_obj = Post.objects.get(owner=self.user)
        count = updated_post_obj.spaces.count()
        self.assertEqual(count, 0)
        with self.assertRaises(Space.DoesNotExist):
            updated_post_obj.spaces.get(name="new_space")

    def test_post_can_have_multiple_spaces(self):
        """Assert that post can have more than 1 space"""
        new_space1 = Space.objects.create(name="new_space1")
        new_space2 = Space.objects.create(name="new_space2")
        self.post.spaces.add(new_space1, new_space2)
        self.post.save()
        updated_post_obj = Post.objects.get(owner=self.user)
        count = updated_post_obj.spaces.count()
        self.assertEqual(count, 2)
        new_space1.delete()
        new_space2.delete()

    def test_reverse_call_space_post(self):
        """Assert that post can be accessed from space"""
        new_space = Space.objects.create(name="new_space")
        self.post.spaces.add(new_space)
        self.post.save()
        post = new_space.posts.get(owner=self.user)
        self.assertEqual(post, self.post)
        new_space.delete()

    def test_methods(self):
        """Assert that methods are working as expected"""
        other_user = User.objects.create_user(
            username="other" + username, email="other_" + email, password=password
        )
        self.post.bookmarks.add(other_user)
        self.post.likes.add(other_user)
        self.post.dislikes.add(other_user)
        self.post.save()
        updated_post = Post.objects.get(owner=self.user)
        like_count = updated_post.likes.count()
        dislike_count = updated_post.dislikes.count()
        bookmark_count = updated_post.bookmarks.count()
        self.assertEqual(updated_post.total_likes(), like_count)
        self.assertEqual(updated_post.total_dislikes(), dislike_count)
        self.assertEqual(updated_post.total_bookmarks(), bookmark_count)
        other_user.delete()
