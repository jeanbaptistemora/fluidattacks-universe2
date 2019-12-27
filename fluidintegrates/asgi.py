"""
ASGI config for fluidintegrates project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/asgi/
"""

import os

import django
from channels.routing import ProtocolTypeRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fluidintegrates.settings")
django.setup()

# pylint: disable=invalid-name
application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
})
