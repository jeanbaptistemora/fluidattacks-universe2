import os
import sys
from django.core.wsgi import get_wsgi_application


# Calculate the path based on the location of the WSGI script.
APACHE_CONF = os.path.dirname(__file__)
PROJECT = os.path.dirname(APACHE_CONF)
WORKSPACE = os.path.dirname(PROJECT)
sys.path.append(WORKSPACE)
sys.path.append(PROJECT)

# Add the path to 3rd party django application and to django itself.
sys.path.append('/usr/src/app')
os.environ['DJANGO_SETTINGS_MODULE'] = 'fluidintegrates.apache.override'

# pylint: disable=invalid-name
application = get_wsgi_application()
