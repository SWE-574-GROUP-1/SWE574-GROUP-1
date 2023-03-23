"""Contains utility methods for Post model"""
from ...models import Post, Profile, Tag, Space
from django.http import HttpResponseRedirect
from django.contrib import messages
from ..utils.generate_preview import generate_preview_


def create_post(request: object) -> None:
    """
    Implementation of creating a Post model and saving it to database
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: None
    """
    # Get the username of the user that requests to create a post
    owner_username = request.user.username
    owner = request.user
    # Get preview details
    preview = generate_preview_(url=request.POST.get('link'))
    print(preview.get('description'))
    print(type(preview.get('description')))
    # Creating new post
    if preview:
        new_post = Post.objects.create(owner_username=owner_username,
                                       owner=owner,
                                       link=request.POST.get("link"),
                                       caption=request.POST.get("caption"),
                                       title=preview.get('title'),
                                       description=preview.get('description'),
                                       preview_image=preview.get('image')
                                       )
    else:
        print("HI FROM ELSE")
        new_post = Post.objects.create(owner_username=owner_username,
                                       owner=owner,
                                       link=request.POST.get("link"),
                                       caption=request.POST.get("caption"),
                                       )
    print(['tag' in key for key in list(request.POST.keys())],
          type(request.POST.keys()), )
    for key in list(request.POST.keys()):
        if 'tag' in key:
            # Get the tag name
            print(key)
            tag_name = request.POST.get(key)
            print(tag_name)
            # Get the Tag object
            tag = Tag.objects.get(name=tag_name)
            new_post.tags.add(tag)
    space_name = request.POST.get('space')
    if space_name:
        space = Space.objects.get(name=space_name)
        new_post.spaces.add(space)
    print(request.POST)
    new_post.save()
    # Print the tags
    for tag in new_post.tags.all():
        print(tag.name)
    pass


def update_post(request: object) -> None:
    """
    Implementation of updating an existing a Post model and saving the updated version to database
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: None
    """
    # Get the existing post
    current_post = Post.objects.get(post_id=request.POST.get("post_id"))
    # Extract fields from request
    link = request.POST.get('link')
    caption = request.POST.get("caption")
    # Modify existing post
    if link:
        current_post.link = link
    if caption:
        current_post.caption = caption
    preview = generate_preview_(url=link)
    if preview:
        current_post.title = preview.get('title')
        current_post.description = preview.get('description')
        current_post.preview_image = preview.get('image')
    # Reset the tags
    current_post.tags.clear()
    # Reassign the keys
    for key in list(request.POST.keys()):
        if 'tag' in key:
            # Get the tag name
            tag_name = request.POST.get(key)
            # Get the Tag object
            tag = Tag.objects.get(name=tag_name)
            current_post.tags.add(tag)
    space_name = request.POST.get('space')
    if space_name:
        current_post.spaces.clear()
        space = Space.objects.get(name=space_name)
        current_post.spaces.add(space)
    print(request.POST)
    current_post.save()


def __book_post__(request: object) -> HttpResponseRedirect:
    """
    Implementation of booking a Post model. Checks whether the post already booked or not and pass the redirection
    path, post mode and username the corresponding function accordingly
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: Redirects the user to the current page
    """
    try:

        id_user = Profile.objects.get(user=request.user).id_user
        print("Post created by username:", id_user)
        # Get the Post model by post_id
        post_id = request.GET.get('post_id')
        post = Post.objects.get(post_id=post_id)
        print("post is", post)
        path = request.META.get('HTTP_REFERER')
        # Control whether bookmarked or not
        if id_user in post.bookmarked_by:
            return un_bookmark_post(path=path, post=post, id_user=id_user)
        else:
            return bookmark_post(path=path, post=post, id_user=id_user)
    except Exception as e:
        print("Error is:", e)
        raise e


def bookmark_post(path, post: Post, id_user: int) -> HttpResponseRedirect:
    """
    Implementation of bookmarking of a Post model. Appends the username to the bookmarked_by attribute of the post and
    increases num_of_bookmarks by 1
    @param path: Redirection path after bookmarking is performed
    @param post: Post model to be bookmarked
    @param username: username of the owner of the Post
    @return: Redirects the user to the current page
    """
    print("Bookmarked")
    post.bookmarked_by.append(id_user)
    post.num_of_bookmarks += 1
    post.save()
    return HttpResponseRedirect(path)


def un_bookmark_post(path, post: Post, id_user: int):
    """
    Implementation of un-bookmarking of a Post model. Removes the username to the bookmarked_by attribute of the post and
    decreases num_of_bookmarks by 1
    @param path: Redirection path after un-bookmarking is performed
    @param post: Post model to be bookmarked
    @param username: username of the owner of the Post
    @return: Redirects the user to the current page
    """
    print("De-bookmarked")
    post.bookmarked_by.remove(id_user)
    post.num_of_bookmarks -= 1
    post.save()
    return HttpResponseRedirect(path)


def __delete_post__(request: object) -> HttpResponseRedirect:
    """
    Implementation of deleting a Post model from database.
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: Redirects the user to the current page
    """
    try:
        post_id = request.GET.get('post_id')
        # Delete the Post
        post = Post.objects.filter(post_id=post_id)
        post.delete()
        messages.success(request, "The Post is deleted")
    except Exception as e:
        print("Error is:", e)
    redirect_path = '/profile/'+request.user.username
    return HttpResponseRedirect(redirect_path)
