import os
import sys
from jinja2 import Environment, FileSystemLoader, select_autoescape

j2_env = Environment(loader=FileSystemLoader('/usr/src/app/deploy/containers/common/vars'),
                     trim_blocks=True, autoescape=select_autoescape(['html', 'xml']))

context = {
    'documentroot': '/usr/src/app/',

}

ssl = j2_env.get_template('integrates-ssl.j2')
ssl.stream(context).dump('integrates-ssl.conf')
if sys.argv[1] == 'development':
    default = j2_env.get_template('default_dev.j2')
else:
    default = j2_env.get_template('default_prod.j2')
default.stream(context).dump('000-default.conf')

os.rename('integrates-ssl.conf', \
'/etc/apache2/sites-available/integrates-ssl.conf')
os.rename('000-default.conf', \
'/etc/apache2/sites-available/000-default.conf')
