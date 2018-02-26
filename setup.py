#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from setuptools import setup
from setuptools.command.test import test as testCommand

import health_check_plus


class Tox(testCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        testCommand.initialize_options(self)
        self.tox_args = ''

    def finalize_options(self):
        testCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)

setup(
    name='django-health-check-plus',
    version=health_check_plus.__version__,
    description=health_check_plus.__description__,
    long_description='Django package to improve usage of django-health-check library.',
    author=health_check_plus.__author__,
    author_email=health_check_plus.__email__,
    url=health_check_plus.__url__,
    packages=[
        'health_check_plus',
    ],
    include_package_data=True,
    install_requires=['django-health-check>=1.0.2,<=1.3.0'],
    license=health_check_plus.__license__,
    zip_safe=False,
    keywords='python, django, health, check, network, service',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='tests',
    tests_require=['tox', 'Django'],
    cmdclass={'test': Tox},
)
