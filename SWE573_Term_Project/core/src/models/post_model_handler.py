"""Contains utility methods for Post model"""
from ...models import Post
from django.http import HttpResponseRedirect
from django.contrib import messages


def create_post(request: object) -> None:
    """
    Implementation of creating a Post model and saving it to database
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: None
    """
    # Get the username of the user that requests to create a post
    owner_username = request.user.username

    # Creating new post
    new_post = Post.objects.create(owner_username=owner_username,
                                   link=request.POST.get("link"),
                                   caption=request.POST.get("caption"))
    new_post.save()
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
    current_post.save()


def __book_post__(request: object) -> HttpResponseRedirect:
    """
    Implementation of booking a Post model. Checks whether the post already booked or not and pass the redirection
    path, post mode and username the corresponding function accordingly
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: Redirects the user to the current page
    """
    try:
        username = request.user.username
        print("Post created by username:", username)
        # Get the Post model by post_id
        post_id = request.GET.get('post_id')
        post = Post.objects.get(post_id=post_id)
        print("post is", post)
        path = request.META.get('HTTP_REFERER')
        # Control whether bookmarked or not
        if username in post.bookmarked_by:
            return un_bookmark_post(path=path, post=post, username=username)
        else:
            return bookmark_post(path=path, post=post, username=username)
    except Exception as e:
        print("Error is:", e)
        raise e


def bookmark_post(path, post: Post, username: str) -> HttpResponseRedirect:
    """
    Implementation of bookmarking of a Post model. Appends the username to the bookmarked_by attribute of the post and
    increases num_of_bookmarks by 1
    @param path: Redirection path after bookmarking is performed
    @param post: Post model to be bookmarked
    @param username: username of the owner of the Post
    @return: Redirects the user to the current page
    """
    print("Bookmarked")
    post.bookmarked_by.append(username)
    post.num_of_bookmarks += 1
    post.save()
    return HttpResponseRedirect(path)


def un_bookmark_post(path, post: Post, username: str):
    """
    Implementation of un-bookmarking of a Post model. Removes the username to the bookmarked_by attribute of the post and
    decreases num_of_bookmarks by 1
    @param path: Redirection path after un-bookmarking is performed
    @param post: Post model to be bookmarked
    @param username: username of the owner of the Post
    @return: Redirects the user to the current page
    """
    print("De-bookmarked")
    post.bookmarked_by.remove(username)
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
    redirect_path = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(redirect_path)
