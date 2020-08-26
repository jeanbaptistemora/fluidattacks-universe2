FROM alpine:3.8

ENV FLAVOR weak

EXPOSE 53/tcp 53/udp

RUN apk update && apk upgrade && apk add bind

COPY named.conf /etc/bind/named.conf
COPY named.conf.options.weak /etc/bind/named.conf.options
COPY named.conf.local.weak /etc/bind/named.conf.local
RUN mkdir -p /var/bind
COPY db.test.weak /var/bind/db.test
RUN chown root:named /var/bind/ /etc/bind -R

CMD /usr/sbin/named -g
