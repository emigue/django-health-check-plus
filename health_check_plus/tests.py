from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse


class StatusOptionalCheckViewTest(TestCase):
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
