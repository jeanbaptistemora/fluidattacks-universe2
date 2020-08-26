FROM alpine:latest

EXPOSE 80

RUN apk update && apk upgrade && mkdir -p /run/apache2 && apk add apache2

CMD /usr/sbin/httpd -D FOREGROUND
