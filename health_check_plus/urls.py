from django.conf.urls import url

from health_check_plus.views import StatusOptionalCheckView

urlpatterns = [
    url(r'^ping/$', StatusOptionalCheckView.as_view(), name='health_optional_check'),
]
