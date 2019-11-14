import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

j2_env = Environment(loader=FileSystemLoader('/usr/src/app/deploy/containers/common/vars'),
                     trim_blocks=True, autoescape=select_autoescape(['html', 'xml']))

context = {
    'DRIVE_AUTHORIZATION': os.environ['FI_DRIVE_AUTHORIZATION'],
    'documentroot': '/usr/src/app/',
    'DRIVE_AUTHORIZATION_CLIENT': os.environ['FI_DRIVE_AUTHORIZATION_CLIENT'],

}
drive = j2_env.get_template('drive_authorization.j2')
drive.stream(context).dump('drive_authorization.json')
ssl = j2_env.get_template('integrates-ssl.j2')
ssl.stream(context).dump('integrates-ssl.conf')
default = j2_env.get_template('default.j2')
default.stream(context).dump('000-default.conf')
client = j2_env.get_template('drive_client_secret.j2')
client.stream(context).dump('drive_client_secret.json')

os.rename('drive_authorization.json', \
'/usr/src/app/config/drive_authorization.json')
os.rename('drive_client_secret.json', \
'/usr/src/app/config/drive_client_secret.json')
os.rename('integrates-ssl.conf', \
'/etc/apache2/sites-available/integrates-ssl.conf')
os.rename('000-default.conf', \
'/etc/apache2/sites-available/000-default.conf')
