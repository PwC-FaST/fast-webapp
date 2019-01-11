"""
WSGI config for fast_web_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from configurations import importer
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fast_web_backend.settings")
os.environ.setdefault('DJANGO_CONFIGURATION', 'Prod')

importer.install()

application = get_wsgi_application()
