#!/usr/bin/env python
import sys
import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line

urlpatterns = []


DEBUG = True
TEMPLATE_DEBUG = DEBUG
BASE_DIR = os.path.dirname(__file__)
ROOT_URLCONF = __name__
SECRET_KEY = 'qwerty'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
}]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

INSTALLED_APPS = [
    'django_nose',
    'redisca.admin_sidebar',
    'redisca.template',
    'redisca.seo',
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


def main():
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    settings.configure(**globals())
    django.setup()

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
