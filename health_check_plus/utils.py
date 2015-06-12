import json
import decimal
from django.http import HttpResponse


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    return unicode(obj)


class JsonResponse(HttpResponse):

    def __init__(self, object, ensure_ascii=True, **kwargs):
        content = json.dumps(object, ensure_ascii=ensure_ascii, default=decimal_default)
        super(JsonResponse, self).__init__(content, mimetype='application/json', **kwargs)