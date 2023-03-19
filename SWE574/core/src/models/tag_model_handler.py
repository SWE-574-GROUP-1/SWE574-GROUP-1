from ...models import Tag, Post


def create_tag(request: object) -> None:
    # TODO: Implement created/already exist Message, create a rule for tag names maybe?
    try:
        tag_name = request.POST.get("tag_name")
        tag = Tag.objects.create(name=tag_name)
        tag.save()
        # Message success here
    except Exception as e:
        # Message failure here
        pass


def reset_tags(post: Post):
    post.tags.clear()
    post.save()


def validate_tag(request: object):
    # Validate does not exist
    tag_name = request.POST.get("tag_name")
    if Tag.objects.filter(name=tag_name).exists():
        print("Tag already exist")
        return False
    else:
        print("Tag name is valid")
        return True
