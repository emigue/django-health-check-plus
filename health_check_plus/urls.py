from django.conf.urls import patterns, url

import health_check
health_check.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'health_check_plus.views.main', name='health_check_plus_main'),
)
