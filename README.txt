1)
apt remove apache2 && apt purge apache2 
sudo apt install git python python-pip apache2 libapache2-mod-python libapache2-mod-wsgi libapache2-mod-wsgi-py3
pip install --upgrade pip
#opcional para python-pptx
sudo apt install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
sudo pip install django requests openpyxl lxml python-pptx pyyaml decorators
2)
cd /var/www && sudo git clone https://glopezfluid@bitbucket.org/fluidsignal/fluid-integrates.git
cd fluid-integrates && sudo mkdir logs && touch /var/www/fluid-integrates/logs/error.err && touch /var/www/fluid-integrates/logs/integrates.log && sudo chmod 777 -R logs && ./manage.py makemigrations && ./manage.py migrate && sudo ./manage.py runserver
sudo mkdir /var/www/fluid-integrates/app/autodoc/results && sudo chown www-data:www-data /var/www/fluid-integrates/app/autodoc/results
verificar que /var/www/fluid-integrates/fluidintegrates/apache/override.py {agregar [ip , 'localhost', '127.0.0.1']}
sudo chown www-data:www-data /var/www/fluid-integrates
3)
nano /etc/apache2/sites-available/000-default.conf
<VirtualHost *:80>
    WSGIScriptAlias / /var/www/fluid-integrates/fluidintegrates/apache/wsgi.py
	ServerAdmin glopez@fluid.la
	Alias /assets/ /var/www/fluid-integrates/app/assets/
    <Directory "/var/www/fluid-integrates/fluidintegrates/apache/">
		Require all granted
    </Directory>
	<Directory "/assets/">
		Require all granted
	</Directory>
	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined
	#Headers
</VirtualHost>


