from ...models import Space


def create_space(request: object):
    # TODO: Implement created/already exist Message, create a rule for tag names maybe?
    try:
        space_name = request.POST.get("space_name")
        space = Space.objects.create(name=space_name)
        space.save()
        # Message success here
    except Exception as e:
        print(f"{e=}")
        # Message failure here
        pass


def validate_space(request: object):
    # Validate does not exist
    space_name = request.POST.get("space_name")
    if Space.objects.filter(name=space_name).exists():
        print("Space already exist")
        return False
    else:
        print("Space name is valid")
        return True
