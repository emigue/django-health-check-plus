========================
Django Health Check Plus
========================

:Version: 1.0.1
:Author: Miguel Angel Moreno

Django package to improve usage of django-health-check library.

Install
=======

Install package::

    python setup.py install

Configuration
=============

Include in settings.py the next settings::

    INSTALLED_APPS = (
                        ...,
                        'health_check',
                        ...
                      )

Where name is set by user and plugin_identifier is the identifier given by health_check library for every plugin.

Example::

    INSTALLED_APPS = (
                        ...
                        'health_check',
                        'health_check.celery',
                        'health_check.db',
                        'health_check.cache',
                        'health_check.storage',
                        ...
                      )

Include the next line in urlpatterns variable in urls.py::

    url(r'^status/', include('health_check_plus.urls')),


Add new check
=============

Writing a health check is quick and easy:

.. code:: python

    from health_check.backends import BaseHealthCheckBackend

    class MyHealthCheckBackend(BaseHealthCheckBackend):
        def check_status(self):
            # The test code goes here.
            # You can use `self.add_error` or
            # raise a `HealthCheckException`,
            # similar to Django's form validation.
            pass

        def identifier(self):
            # Might be overridden if you want to get a custom name, otherwise
            # the checker class name will be used.
            return self.__class__.__name__

After writing a custom checker, register it in your app configuration:

.. code:: python

    from django.apps import AppConfig

    from health_check.plugins import plugin_dir

    class MyAppConfig(AppConfig):
        name = 'my_app'

        def ready(self):
            from .backends import MyHealthCheckBackend
            plugin_dir.register(MyHealthCheckBackend)

Make sure the application you write the checker into is registered in your ``INSTALLED_APPS``.

Usage
=====

To show main page of django-health-check library (html) use::

    http://myserver/status/


To show checks status in json format use::

    http://myserver/status?format=json


To show status of one check named 'mycheck' in json format use::

    http://myserver/status?format=json&checks=mycheck

To show status of some checks (mycheck1 and mycheck2) in json format use::

    http://myserver/status?format=json&checks=mycheck1,mycheck2

HTTP status code:

 * 200: If all queried checks are in status OK.
 * 500: If any queried check is WRONG.
