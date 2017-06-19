import json

import django
from django.http import HttpResponse

DJANGO_17_MINOR_VERSION = 7

if django.VERSION[1] == DJANGO_17_MINOR_VERSION:
    from django.http import JsonResponse
else:
    from django.core.serializers.json import DjangoJSONEncoder


    class JsonResponse(HttpResponse):
        def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
            if safe and not isinstance(data, dict):
                raise TypeError('In order to allow non-dict objects to be '
                                'serialized set the safe parameter to False')
            if 'mimetype' in kwargs:
                raise TypeError('To keep code clean to Django 1.7 JsonResponse do '
                                'not allow mimetype argument since 1.7 version')

            kwargs.setdefault('content_type', 'application/json')
            data = json.dumps(data, cls=encoder)
            super(JsonResponse, self).__init__(content=data, **kwargs)
