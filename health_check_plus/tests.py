from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse

from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import ServiceUnavailable
from health_check.plugins import plugin_dir


class StatusOptionalCheckViewTest(TestCase):
    class ServiceDownCustomHealthCheck(BaseHealthCheckBackend):
        def check_status(self):
            raise ServiceUnavailable('Testing service not working')

    class ServiceUpCustomHealthCheck(BaseHealthCheckBackend):
        def check_status(self):
            pass

    class ServiceUpOverriddenIdentifierCustomHealthCheck(BaseHealthCheckBackend):
        def check_status(self):
            pass

        @staticmethod
        def identifier():
            return 'test_check'

    url = reverse('health_optional_check')

    def test_query_url_with_not_params_returns_html(self):
        result = self.client.get('{}?checks'.format(self.url))

        self.assertEqual(result.status_code, 200)
        with self.assertRaises(ValueError,
                               msg='Content-Type header is "text/html; charset=utf-8", not "application/json"'):
            result.json()

    def test_query_url_with_format_json_returns_json(self):
        result = self.client.get('{}?format=json&checks'.format(self.url))

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), {})

    @override_settings(INSTALLED_APPS=settings.INSTALLED_APPS + ['health_check.db'])
    def test_checks_db_returns_db_status(self):
        result = self.client.get('{}?format=json&checks=db'.format(self.url))

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.json()['DatabaseBackend'], 'unavailable: Database error')

    @override_settings(INSTALLED_APPS=settings.INSTALLED_APPS + ['health_check.db'])
    def test_even_if_db_crash_checks_returns_ok(self):
        result = self.client.get('{}?format=json&checks=cache'.format(self.url))

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), {})

    @override_settings(INSTALLED_APPS=settings.INSTALLED_APPS + ['health_check.db'])
    def test_if_no_checks_in_params_it_checks_all(self):
        result = self.client.get('{}?format=json'.format(self.url))

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.json()['DatabaseBackend'], 'unavailable: Database error')

    def test_custom_health_check_not_failing(self):
        plugin_dir.register(self.ServiceUpCustomHealthCheck)

        result = self.client.get('{}?format=json&checks=ServiceUpCustomHealthCheck'.format(self.url))

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), {'ServiceUpCustomHealthCheck': 'working'})

    def test_custom_health_check_failing(self):
        plugin_dir.register(self.ServiceDownCustomHealthCheck)

        result = self.client.get('{}?format=json&checks=ServiceDownCustomHealthCheck'.format(self.url))

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.json(), {'ServiceDownCustomHealthCheck': 'unavailable: Testing service not working'})

    def test_custom_health_overridden_identifier_check_not_failing(self):
        plugin_dir.register(self.ServiceUpOverriddenIdentifierCustomHealthCheck)

        result = self.client.get('{}?format=json&checks=test_check'.format(self.url))

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), {'test_check': 'working'})

    def test_two_custom_health_check_one_down_other_up(self):
        plugin_dir.register(self.ServiceUpCustomHealthCheck)
        plugin_dir.register(self.ServiceDownCustomHealthCheck)

        result = self.client.get(
            '{}?format=json&checks=ServiceUpCustomHealthCheck,ServiceDownCustomHealthCheck'.format(self.url))

        self.assertEqual(result.status_code, 500)
        self.assertEqual(
            result.json(),
            {
                'ServiceDownCustomHealthCheck': 'unavailable: Testing service not working',
                'ServiceUpCustomHealthCheck': 'working'
            }
        )


class StatusCheckPingViewTest(TestCase):
    url = reverse('health_check_ping')

    def test_query_url_with_returns_always_json(self):
        result = self.client.get('{}'.format(self.url))

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), {})

    @override_settings(INSTALLED_APPS=settings.INSTALLED_APPS + ['health_check.db'])
    def test_even_if_db_check_enabled_does_not_matter_it_returns_200_anyway(self):
        result = self.client.get('{}'.format(self.url))

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), {})
