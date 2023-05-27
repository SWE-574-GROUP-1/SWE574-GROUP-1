"""Contains utility methods for Post model"""
from ...models import Post, Tag, Space, SemanticTag
from django.http import HttpResponseRedirect
from django.contrib import messages
from ..utils.generate_preview import generate_preview_


def create_post(request: object) -> None:
    """
    Implementation of creating a Post model and saving it to database
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: None
    """
    # Get the user that requests to create a post
    owner = request.user
    # Get preview details
    preview = generate_preview_(url=request.POST.get('link'))
    # Creating new post
    if preview:
        new_post = Post.objects.create(owner=owner,
                                       link=request.POST.get("link"),
                                       caption=request.POST.get("caption"),
                                       title=preview.get('title'),
                                       description=preview.get('description'),
                                       preview_image=preview.get('image')
                                       )
    else:
        new_post = Post.objects.create(owner=owner,
                                       link=request.POST.get("link"),
                                       caption=request.POST.get("caption"),
                                       )

    tags = request.POST.getlist('tags[]')
    for tagId in tags:
        """ if tagId is not a number, it means that the tag is not in the database. So, we need to create a new tag """
        if not tagId.isdigit():
            tag = Tag.objects.create(name=tagId)
        else:
            tag = Tag.objects.get(id=tagId)

        new_post.tags.add(tag)

    semantic_tags = request.POST.getlist('semanticTagValues[]')
    semantic_tag_labels = request.POST.getlist('semanticTagLabels[]')
    for value in semantic_tags:
        wikidata_id = value.split("|")[0]
        label = value.split("|")[1]
        description = value.split("|")[2]
        custom_label = semantic_tag_labels[semantic_tags.index(value)]

        new_semantic_tag = SemanticTag.objects.create(wikidata_id=wikidata_id, label=label, description=description,
                                                      custom_label=custom_label, post=new_post)
        new_post.semantic_tags.add(new_semantic_tag)

    spaces = request.POST.getlist('spaces[]')
    if spaces:
        for space in spaces:
            space = Space.objects.get(name=space)
            new_post.spaces.add(space)
    new_post.save()
    # Print the tags


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
    preview_image = request.POST.get("preview_image")
    # Modify existing post
    if link:
        current_post.link = link
    if caption:
        current_post.caption = caption
    preview = generate_preview_(url=link)
    if preview:
        current_post.title = preview.get('title')
        current_post.description = preview.get('description')
        if not preview_image:
            current_post.preview_image = preview.get('image')
        else:
            current_post.preview_image = preview_image
    # Reset the tags
    current_post.tags.clear()
    # Reassign the keys
    tags = request.POST.getlist('tags[]')
    for tagId in tags:
        """ if tagId is not a number, it means that the tag is not in the database. So, we need to create a new tag """
        if not tagId.isdigit():
            tag = Tag.objects.create(name=tagId)
        else:
            tag = Tag.objects.get(id=tagId)

        current_post.tags.add(tag)

    current_post.semantic_tags.all().delete()

    semantic_tags = request.POST.getlist('semanticTagValues[]')
    semantic_tag_labels = request.POST.getlist('semanticTagLabels[]')
    for value in semantic_tags:
        wikidata_id = value.split("|")[0]
        label = value.split("|")[1]
        description = value.split("|")[2]
        custom_label = semantic_tag_labels[semantic_tags.index(value)]

        new_semantic_tag = SemanticTag.objects.create(wikidata_id=wikidata_id, label=label, description=description,
                                                      custom_label=custom_label, post=current_post)

        current_post.semantic_tags.add(new_semantic_tag)

    space_names = request.POST.getlist('spaces[]')
    if space_names:
        current_post.spaces.clear()
        for space_name in space_names:
            space = Space.objects.get(name=space_name)
            current_post.spaces.add(space)
    current_post.save()


def __book_post__(request: object) -> HttpResponseRedirect:
    """
    Implementation of booking a Post model. Checks whether the post already booked or not and pass the redirection
    path, post mode and username the corresponding function accordingly
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: Redirects the user to the current page
    """
    try:

        id = request.user.id
        print("Post created by username:", id)
        # Get the Post model by post_id
        post_id = request.GET.get('post_id')
        post = Post.objects.get(post_id=post_id)
        print("post is", post)
        path = request.META.get('HTTP_REFERER')
        # Control whether bookmarked or not
        if id in post.bookmarked_by:
            return un_bookmark_post(path=path, post=post, id=id)
        else:
            return bookmark_post(path=path, post=post, id=id)
    except Exception as e:
        print("Error is:", e)
        raise e


def bookmark_post(path, post: Post, id: int) -> HttpResponseRedirect:
    """
    Implementation of bookmarking of a Post model. Appends the username to the bookmarked_by attribute of the post and
    increases num_of_bookmarks by 1
    @param path: Redirection path after bookmarking is performed
    @param post: Post model to be bookmarked
    @param id: id of the owner user of the Post
    @return: Redirects the user to the current page
    """
    print("Bookmarked")
    post.bookmarked_by.append(id)
    post.num_of_bookmarks += 1
    post.save()
    return HttpResponseRedirect(path)


def un_bookmark_post(path, post: Post, id: int):
    """
    Implementation of un-bookmarking of a Post model. Removes the username to the bookmarked_by attribute of the post
    and decreases num_of_bookmarks by 1
    @param path: Redirection path after un-bookmarking is performed
    @param post: Post model to be bookmarked
    @param int id: id of the owner user of the Post
    @return: Redirects the user to the current page
    """
    print("De-bookmarked")
    post.bookmarked_by.remove(id)
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
    redirect_path = '/profile/' + request.user.username
    return HttpResponseRedirect(redirect_path)
