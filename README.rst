========================
Django Health Check Plus
========================

:Version: 0.1.1
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

