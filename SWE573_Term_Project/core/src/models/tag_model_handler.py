from ...models import Tag

def create_tag(request: object) -> None:
    """
    Implementation of creating a Profile model.
    @param request: HttpRequest object that contains metadata about request passed from frontend
    @return: None
    """
    tag_names = request.POST.get("tag-names")
    for tag_name in tag_names:
        tag = Tag.objects.create(name=tag_name)
        tag.save()
