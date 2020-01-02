"""
ASGI config for fluidintegrates project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/asgi/
"""

import os

import django
import newrelic.agent


# pylint: disable=unused-argument
def convert_to_web_transaction(*args, **kwargs):
    newrelic.agent.set_background_task(False)


from django.conf import settings  # noqa: E402

# Init New Relic agent
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fluidintegrates.settings")
django.setup()
NEW_RELIC_CONF_FILE = os.path.join(settings.BASE_DIR, 'newrelic.ini')
newrelic.agent.initialize(NEW_RELIC_CONF_FILE)

import django.core.handlers.base as handlers  # noqa: E402
newrelic.agent.wrap_pre_function(handlers, 'BaseHandler.get_response',
                                 convert_to_web_transaction)
newrelic.agent.wrap_background_task(handlers, 'BaseHandler.get_response')

from channels.routing import ProtocolTypeRouter  # noqa: E402


# pylint: disable=invalid-name
application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
})
