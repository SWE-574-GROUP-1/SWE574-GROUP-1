from ...models import Post
from django.http import HttpResponseRedirect
from django.contrib import messages

def create_post(request):
    # Get the username of the user that requests to create a post
    owner_username = request.user.username
    # Creating new post
    new_post = Post.objects.create(owner_username=owner_username,
                                   link=request.POST.get("link"),
                                   caption=request.POST.get("caption"))
    new_post.save()
    pass


def update_post(request):
    # Get the existing post
    current_post = Post.objects.get(post_id=request.POST.get("post_id"))
    # Modify existing post
    current_post.link = request.POST.get("link")
    current_post.caption = request.POST.get("caption")
    current_post.save()
    pass

def __book_post__(request):
    try:
        username = request.user.username
        print("Post created by username:", username)
        post_id = request.GET.get('post_id')
        post = Post.objects.get(post_id=post_id)
        print("post is", post)
        path = request.META.get('HTTP_REFERER')
        if username in post.bookmarked_by:
            return un_bookmark_post(path=path, post=post, username=username)
        else:
            return bookmark_post(path=path, post=post, username=username)
    except Exception as e:
        print("Error is:", e)
        raise e

def bookmark_post(path ,post: Post, username: str):
    print("Bookmarked")
    post.bookmarked_by.append(username)
    post.num_of_bookmarks += 1
    post.save()
    return HttpResponseRedirect(path)

def un_bookmark_post(path, post: Post, username: str):
    print("De-bookmarked")
    post.bookmarked_by.remove(username)
    post.num_of_bookmarks -= 1
    post.save()
    return HttpResponseRedirect(path)


def __delete_post__(request):
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