from uuid import uuid4
from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel
from django.core.validators import URLValidator
from django.contrib.postgres.fields import ArrayField


# override the default user model
class User(User):
    class Meta:
        proxy = True


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(default="Write something here", max_length=100)
    profile_image = models.ImageField(upload_to="profile_images", default="profile_images/blank-profile-picture.png")
    background_image = models.ImageField(upload_to="background_images",
                                         default="background_images/bg-image-5.jpg")
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False)
    available_labels = ArrayField(models.CharField(max_length=255), default=list, blank=True)

    def __str__(self):
        return self.user.username

    def all_labels(self):
        bookmarks = Bookmark.objects.filter(user=self.user)
        unique_labels = bookmarks.values_list('label_name', flat=True).distinct()
        return unique_labels

    def all_spaces(self):
        return Space.objects.all()

    # Overwrite delete method since OneToOne relationship does not delete User, Either we should use ForeignKey or
    # See: https://stackoverflow.com/questions/12754024/onetoonefield-and-deleting
    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

    def sorted_posts_all(self):
        """Returns all posts of the profile in ascending order by edit date"""
        return self.user.posts.all().order_by("-modified")

    def sorted_bookmarked_posts_all(self):
        return self.user.posts_bookmarked.all().order_by("-modified")


class Post(TimeStampedModel):
    # Fields that are automatically filled
    post_id = models.UUIDField(primary_key=True, default=uuid4, unique=True)
    # likes with created
    likes = models.ManyToManyField(User, related_name='liked_posts', through='Like')
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', through='Dislike')
    # bookmarks with created
    bookmarks = models.ManyToManyField(User, related_name='bookmarked_posts', through='Bookmark')
    # posts must belong to a user
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', blank=False)
    # Fields that are filled by owner user
    link = models.URLField(blank=False, validators=[URLValidator])
    caption = models.TextField(blank=True)  # Caption can be empty
    # Preview attributes
    title = models.TextField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    preview_image = models.TextField(max_length=200, blank=True)
    # Many-to-many field for tags
    tags = models.ManyToManyField('Tag', related_name='posts', default=None)
    spaces = models.ManyToManyField('Space', related_name='posts', default=None)
    # Many-to-many field for comments
    comments = models.ManyToManyField(User, related_name='commented_posts', through='Comment')

    def __str__(self):
        return self.owner.username

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def total_bookmarks(self):
        return self.bookmarks.count()

    def tags_as_json_string(self):
        """ name: tag_name, id: tag_id """
        return [{"name": tag.name, "id": tag.id} for tag in self.tags.all()]

    def semantic_tags_as_json_string(self):
        """ name: tag_name, id: tag_id """
        return [{"id": tag.id, "wikidata_id": tag.wikidata_id, "label": tag.label,
                 "description": tag.description, "custom_label": tag.custom_label} for tag in self.semantic_tags.all()]

    def spaces_as_json_string(self):
        return [{"name": space.name, "id": space.id} for space in self.spaces.all()]

    def __setattr__(self, name, value):
        """Override __setattr_ method to freeze post_id, owner attributes"""
        if name == 'post_id':
            try:
                if value != self.post_id:
                    return
            except ValueError:
                pass
            except AttributeError:
                pass
            except Post.DoesNotExist:
                pass
        if name == 'owner':
            try:
                if value != self.owner:
                    return
            except Post.DoesNotExist:
                pass
        if name == 'link':
            if value == "":
                return

        super(self.__class__, self).__setattr__(name, value)

    def get_comments(self):
        return Comment.objects.filter(post=self)

    def self_label(self):
        """Get the bookmark label for a specific user. If the user has not bookmarked this post, return None."""
        bookmark = Bookmark.objects.filter(user=self.owner, post=self).first()
        return bookmark.label_name if bookmark else None


class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='commented_by_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_commented')
    content = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.content}"

    def self_label(self):
        """Get the bookmark label for a specific user. If the user has not bookmarked this post, return None."""
        bookmark = Bookmark.objects.filter(user=self.owner, post=self).first()
        return bookmark.label_name if bookmark else None


class Like(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_by_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_liked')

    def __str__(self):
        return self.user.username


class Bookmark(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarked_by_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_bookmarked')
    label_name = models.CharField(max_length=25, blank=False, default="default")

    def __str__(self):
        return self.user.username


class Dislike(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='disliked_by_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_disliked')

    def __str__(self):
        return self.user.username


class Tag(TimeStampedModel):
    name = models.CharField(max_length=25, unique=True)


class SemanticTag(TimeStampedModel):
    wikidata_id = models.CharField(max_length=25, unique=False)
    label = models.CharField(max_length=200, unique=False)
    description = models.CharField(max_length=500, unique=False)
    custom_label = models.CharField(max_length=200, unique=False, blank=True)
    """ belongs to one post, post has many semantic tags """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='semantic_tags', unique=False,
                             blank=False, default=1)


class Space(TimeStampedModel):
    name = models.CharField(max_length=25, unique=True)
    avatar = models.ImageField(upload_to="space_images", default="space_images/default_space.jpg")
    description = models.CharField(max_length=100, blank=False, default="This is a Space!")
    subscribers = models.ManyToManyField(User, related_name='subscribed_users', through='Subscriber')


class Subscriber(TimeStampedModel):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='subscribed_by_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spaces_subscribed')
