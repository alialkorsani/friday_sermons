"""
ASGI config for friday_sermon project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'friday_sermon.settings')

application = get_asgi_application()

from django_simple_task import django_simple_task_middlware

application = django_simple_task_middlware(application)
