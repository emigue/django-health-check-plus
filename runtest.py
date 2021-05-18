import django
import sys

from django.conf import settings
from django.test.runner import DiscoverRunner

settings.configure(
    DEBUG=True,
    SECRET_KEY='secret_key',
    ROOT_URLCONF='health_check_plus.urls',
    INSTALLED_APPS=[
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'health_check',
       'health_check_plus'],
    MIDDLEWARE=[],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'sqlite3'
        }
    },
    ALLOWED_HOSTS=['*'],
    TEST_RUNNER='runtest.NoDbTestRunner',
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        }
    ]
)

django.setup()
test_runner = DiscoverRunner(verbosity=1)

failures = test_runner.run_tests(['health_check_plus'])
if failures:
    sys.exit(failures)
