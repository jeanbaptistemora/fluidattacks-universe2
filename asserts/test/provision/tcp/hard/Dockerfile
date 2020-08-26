FROM alpine:latest

EXPOSE 443

RUN apk update && apk upgrade && mkdir -p /run/apache2 && apk add apache2-ssl

CMD /usr/sbin/httpd -D FOREGROUND
