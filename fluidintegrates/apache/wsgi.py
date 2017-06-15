import os
import sys
from django.core.wsgi import get_wsgi_application


# Calculate the path based on the location of the WSGI script.
apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)
sys.path.append(project)

# Add the path to 3rd party django application and to django itself.
sys.path.append('/usr/src/app')
os.environ['DJANGO_SETTINGS_MODULE'] = 'fluidintegrates.apache.override'


application = get_wsgi_application()
