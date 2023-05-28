
""" annotation controller """
import requests
from django.http import JsonResponse
import json
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import uuid
import os
import environ

# read environment variables
current_directory = os.getcwd()
env = environ.Env()
environ.Env.read_env('/app/LinkMe/.env')


@csrf_exempt
def create_annotation(request):
    if request.method == 'POST':
        # Access the request body
        body = request.body.decode('utf-8')
        annotation = json.loads(body)
        """ if isset annotation['image_selection'] """
        if 'image_selection' in annotation:
            return convert_image_annotation_to_ldp_format(request, annotation)
        else:
            return convert_text_annotation_to_ldp_format(request, annotation)

        return JsonResponse({'status': 'fail'}, safe=False)


def convert_image_annotation_to_ldp_format(request, annotation):
    random_uuid = uuid.uuid4()

    annotation_ldp = {
        "@context": "http://www.w3.org/ns/anno.jsonld",
        "id": annotation['uri'] + "/annotations/" + str(random_uuid),
        "type": "Annotation",
        "motivation": "highlighting",
        "created": timezone.now().isoformat(),
        "target": {
            "source": annotation['image_selection']['src'],
            "selector": {
                "type": "FragmentSelector",
                "conformsTo": "http://www.w3.org/TR/media-frags/",
                "value": "xywh=percent:" + annotation['image_selection']['x'] + "," + annotation['image_selection']['y'] + "," + annotation['image_selection']['w'] + "," + annotation['image_selection']['h'],
            },
        },
        "body": {
            "type": "TextualBody",
            "value": annotation['text'],
            "format": "text/plain"
        },
        "creator": request.user.id,
    }

    """ send annotation_ldp to ldp server """
    ANNOTATION_URL = env('ANNOTATION_SERVICE_URL')+"/annotations/"
    requests.post(ANNOTATION_URL, json=annotation_ldp)
    return JsonResponse(annotation, safe=False)


def convert_text_annotation_to_ldp_format(request, annotation):
    random_uuid = uuid.uuid4()
    ranges = annotation['ranges'][0]
    referrer = request.META['HTTP_REFERER']
    annotation_ldp = {
        "@context": "http://www.w3.org/ns/anno.jsonld",
        "id": referrer + "/annotations/" + str(random_uuid),
        "type": "Annotation",
        "motivation": "highlighting",
        "created": timezone.now().isoformat(),
        "target": {
            "source": referrer,
            "selector": {
                "type": "RangeSelector",
                "startSelector": {
                    "type": "XPathSelector",
                    "value": ranges['start']
                },
                "endSelector": {
                    "type": "XPathSelector",
                    "value": ranges['end']
                },
                "startOffset": ranges['startOffset'],
                "endOffset": ranges['endOffset']
            }
        },
        "body": {
            "type": "TextualBody",
            "value": annotation['text'],
            "format": "text/plain"
        },
        "creator": request.user.id
    }

    """ send annotation_ldp to ldp server """
    ANNOTATION_URL = env('ANNOTATION_SERVICE_URL')+"/annotations/"
    requests.post(ANNOTATION_URL, json=annotation_ldp)
    return JsonResponse(annotation, safe=False)


def get_annotations(request):
    # read environment variables
    if request.method == 'GET':
        q = request.GET.get('uri')

        annotations = requests.get(env('ANNOTATION_SERVICE_URL')+"/annotations/search?query="+q).json()
        json = {
            "total": len(annotations),
            "rows": []
        }
        for annotation in annotations:
            if annotation['target']['selector']['type'] == "FragmentSelector":
                selector = annotation['target']['selector']['value']
                x = selector.split('=percent:')[1].split(',')[0]
                y = selector.split('=percent:')[1].split(',')[1]
                w = selector.split('=percent:')[1].split(',')[2]
                h = selector.split('=percent:')[1].split(',')[3]
                json['rows'].append({
                    "image_selection": {
                        "src": annotation['target']['source'],
                        "uri": annotation['target']['source'],
                        "x": x,
                        "y": y,
                        "w": w,
                        "h": h,
                    },
                    "text": annotation['body']['value'],
                })
            else:
                json['rows'].append({
                    "quote": annotation['body']['value'],
                    "ranges": [
                        {
                            "start": annotation['target']['selector']['startSelector']['value'],
                            "startOffset": annotation['target']['selector']['startOffset'],
                            "end": annotation['target']['selector']['endSelector']['value'],
                            "endOffset": annotation['target']['selector']['endOffset']
                        }

                    ],
                    "uri": annotation['target']['source'],
                    "text": annotation['body']['value'],
                })

    return JsonResponse(json, safe=False)
