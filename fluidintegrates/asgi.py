"""
ASGI config for fluidintegrates project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/asgi/
"""


import os
from django.core.asgi import get_asgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fluidintegrates.settings")

# pylint: disable=invalid-name
application = get_asgi_application()
