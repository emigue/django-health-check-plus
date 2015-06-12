from django.conf import settings

HEALTH_CHECK_PLUGINS = getattr(settings, 'HEALTH_CHECK_PLUGINS', {})