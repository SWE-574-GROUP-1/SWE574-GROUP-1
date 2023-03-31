# from unittest import TestCase
# from ..models import Post
# from django.core.exceptions import ObjectDoesNotExist
#
# owner_username = "daglar"
# link = "https://docs.djangoproject.com/en/4.1/topics/testing/overview/"
# caption = "This is my test post!"
#
#
# class TestPost(TestCase):
#     def setUp(self):
#         test_post = Post.objects.create(owner_username=owner_username,
#                                         link=link,
#                                         caption=caption)
#         test_post.save()
#
#     # Test Creating Post
#     def test_post_owner_username(self):
#         test_post = Post.objects.filter(owner_username=owner_username)[0]
#         self.assertEqual(test_post.owner_username, owner_username)
#         self.assertNotEqual(test_post.owner_username, owner_username + "s")
#
#     def test_post_link(self):
#         test_post = Post.objects.filter(link=link)[0]
#         self.assertEqual(test_post.link, link)
#         self.assertNotEqual(test_post.link, link + "s")
#
#     def test_post_caption(self):
#         test_post = Post.objects.filter(caption=caption)[0]
#         self.assertEqual(test_post.caption, caption)
#         self.assertNotEqual(test_post.caption, caption + "s")
#
#     def test_post_change_username(self):
#         test_post = Post.objects.filter(owner_username=owner_username)[0]
#         # Change the username
#         new_username = "test_change_username"
#         test_post.owner_username = new_username
#         test_post.save()
#         # Get the changed version
#         test_post = Post.objects.filter(owner_username=new_username)[0]
#         self.assertEqual(test_post.owner_username, new_username)
#
#     def test_post_change_link(self):
#         test_post = Post.objects.filter(link=link)[0]
#         # Change the link
#         new_link = "new_link"
#         test_post.link = new_link
#         test_post.save()
#         # Get the changed version
#         changed_test_post = Post.objects.filter(link=new_link)[0]
#         self.assertEqual(changed_test_post.link, new_link)
#
#     def test_post_change_caption(self):
#         test_post = Post.objects.filter(caption=caption)[0]
#         new_caption = "new_caption"
#         test_post.caption = new_caption
#         test_post.save()
#         # Get the changed version
#         changed_test_post = Post.objects.filter(caption=new_caption)[0]
#         self.assertEqual(changed_test_post.caption, new_caption)
#
#     def test_post_invalid_attr(self):
#         test_post = Post.objects.filter(caption=caption)[0]
#         with self.assertRaises(AttributeError):
#             test_post.invalid_field_1
#             test_post.invalid_field_2
#             test_post.invalid_field_3
#
#     # Test Deleting Model
#     def test_post_delete(self):
#         test_post = Post.objects.filter(owner_username=owner_username)
#         test_post.delete()
#         with self.assertRaises(ObjectDoesNotExist):
#             Post.objects.filter(owner_username=owner_username)
#             Post.objects.get(owner_username=owner_username)
