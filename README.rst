========================
Django Health Check Plus
========================

:Version: 0.2.0
:Status: beta
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
                        'health_check_plus',
                        ...
                      )

Include the next variable in settings.py::

    HEALTH_CHECK_PLUGINS = {
        'name': 'plugin_identifier'
    }

Where name is set by user and plugin_identifier es the identifier given by health_check library for every plugin.

Example::

    INSTALLED_APPS = (
                        ...
                        'health_check',
                        'health_check_plus',
                        'health_check_celery',
                        'health_check_db',
                        'health_check_cache',
                        'health_check_storage',
                        ...
                      )

    HEALTH_CHECK_PLUGINS = {
        'db': 'DjangoDatabaseBackend',
        'cache': 'CacheBackend',
        'celery': 'CeleryHealthCheck',
        'storage': 'DefaultFileStorageHealthCheck'
    }

Include the next line in urlpatterns variable in urls.py::

    url(r'^status/', include('health_check_plus.urls')),


Add new check
=============

Create file in your project named plugin_health_check.py.

Create check class inherited from BaseHealthCheckBackend::

    from health_check.backends.base import BaseHealthCheckBackend
    from health_check.plugins import plugin_dir

    class MyCheckBackend(BaseHealthCheckBackend):

        def check_status(self):
            pass

    plugin_dir.register(MyCheckBackend)


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
 * 500: If some queried check is WRONG.
