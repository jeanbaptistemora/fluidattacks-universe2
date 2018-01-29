import os
import jinja2
from jinja2 import Environment
from jinja2 import FileSystemLoader

j2_env = Environment(loader=FileSystemLoader('/usr/src/app/deploy/containers/common/vars'),
                     trim_blocks=True)

context = {
    'DRIVE_AUTHORIZATION': os.environ['FI_DRIVE_AUTHORIZATION'],
    'documentroot': os.environ['FI_DOCUMENTROOT']

}
drive = j2_env.get_template('drive_authorization.j2')
drive.stream(context).dump('drive_authorization.json')
ssl = j2_env.get_template('integrates-ssl.j2')
ssl.stream(context).dump('integrates-ssl.conf')
default = j2_env.get_template('default.j2')
default.stream(context).dump('000-default.conf')

os.rename('drive_authorization.json', \
'/usr/src/app/config/drive_authorization.json')
os.rename('integrates-ssl.conf', \
'/etc/apache2/sites-available/integrates-ssl.conf')
os.rename('000-default.conf', \
'/etc/apache2/sites-available/000-default.conf')
