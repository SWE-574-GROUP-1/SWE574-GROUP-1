import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def get_title(html):
    """Scrape page title."""
    try:
        title = None
        if html.title.string:
            title = html.title.string
        elif html.find("meta", property="og:title"):
            title = html.find("meta", property="og:title").get('content')
        elif html.find("meta", property="twitter:title"):
            title = html.find("meta", property="twitter:title").get('content')
        elif html.find("h1"):
            title = html.find("h1").string
        return title
    except Exception as e:
        print(f"{e=}")
        return None


def get_description(html):
    """Scrape page description."""
    try:
        description = None
        if html.find("meta", property="description"):
            description = html.find("meta", property="description").get('content')
        elif html.find("meta", property="og:description"):
            description = html.find(
                "meta", property="og:description").get('content')
        elif html.find("meta", property="twitter:description"):
            description = html.find(
                "meta", property="twitter:description").get('content')
        elif html.find("p"):
            description = html.find("p").contents
        return description
    except Exception as e:
        print(f"{e=}")
        return None


def get_image(html):
    """Scrape share image."""
    try:
        image = None
        if html.find("meta", property="image"):
            image = html.find("meta", property="image").get('content')
        elif html.find("meta", property="og:image"):
            image = html.find("meta", property="og:image").get('content')
        elif html.find("meta", property="twitter:image"):
            image = html.find("meta", property="twitter:image").get('content')
        elif html.find("img", src=True):
            image = html.find_all("img").get('src')
        return image
    except Exception as e:
        print(f"{e=}")
        return None


@login_required(login_url="core:signin")
def generate_preview(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    url = request.GET.get('link')
    print("url is:", url)
    req = requests.get(url, headers)
    html = BeautifulSoup(req.content, 'html.parser')
    meta_data = {
        'title': get_title(html),
        'description': get_description(html),
        'image': get_image(html),
    }

    print(meta_data)
    print(type(meta_data))
    print(type(meta_data.get('image')))
    return JsonResponse(meta_data)


def generate_preview_(url: str):
    print("GENERATE_PREVIEW_ IS CALLED!")
    if not url:
        return dict()

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    print("URL is:", url)
    try:
        req = requests.get(url, headers)
        html = BeautifulSoup(req.content, 'html.parser')
        meta_data = {
            'title': get_title(html),
            'description': get_description(html),
            'image': get_image(html),
        }
        print("META_DATA IS:")
        print(meta_data.get('description'))
        if meta_data.get('title') and meta_data.get('description') and meta_data.get('image'):
            return meta_data
        else:
            return dict()
    except Exception as e:
        print(f"{e=}")
        return dict()
