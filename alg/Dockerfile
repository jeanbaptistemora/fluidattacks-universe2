FROM debian:jessie

RUN DEBIAN_FRONTEND=noninteractive apt-get -y update &&\
	DEBIAN_FRONTEND=noninteractive apt-get -y upgrade &&\
	DEBIAN_FRONTEND=noninteractive apt-get -y install apache2 nano &&\
	ln -snf /usr/share/zoneinfo/America/Bogota /etc/localtime && \
	a2enmod rewrite &&\
	a2enmod proxy_http &&\ 
	a2enmod ssl &&\
	a2enmod substitute &&\
	a2enmod headers
    
	
ADD image/apache2.conf /etc/apache2/apache2.conf
ADD image/httpd.conf /etc/apache2/httpd.conf
ADD image/security /etc/apache2/conf.d/security
ADD image/default-ssl /etc/apache2/sites-enabled/default-ssl
ADD image/fluid.la /etc/apache2/sites-enabled/fluid.la
ADD image/mail.fluid.la /etc/apache2/sites-enabled/mail.fluid.la
ADD image/www.fluid.la /etc/apache2/sites-enabled/www.fluid.la
ADD image/web.fluid.la /etc/apache2/sites-enabled/web.fluid.la
ADD image/fluidla.crt /etc/ssl/certs/fluidla.crt
ADD image/fluidla.key /etc/ssl/private/fluidla.key

CMD ["/usr/sbin/apache2ctl", "-D FOREGROUND"]
