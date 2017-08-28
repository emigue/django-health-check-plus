from django.conf.urls import url

from health_check_plus.views import StatusOptionalCheckView, StatusCheckPingView

urlpatterns = [
    url(r'^ping/$', StatusCheckPingView.as_view(), name='health_check_ping'),
    url(r'^status/$', StatusOptionalCheckView.as_view(), name='health_optional_check'),
]
