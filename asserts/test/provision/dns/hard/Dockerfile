FROM registry.gitlab.com/fluidattacks/asserts/mocks/dns:weak

ENV FLAVOR hard

EXPOSE 53/tcp 53/udp

COPY named.conf /etc/bind/named.conf
COPY named.conf.options.hard /etc/bind/named.conf.options
COPY named.conf.local.hard /etc/bind/named.conf.local

RUN mkdir -p /var/bind

COPY Kfluid.la.+007+14480.ky /var/bind
COPY Kfluid.la.+007+14480.private /var/bind
COPY Kfluid.la.+007+26391.ky /var/bind
COPY Kfluid.la.+007+26391.private /var/bind
COPY db.test.signed /var/bind/db.test.signed
RUN chown root:named /var/bind/ /etc/bind -R && \
    chmod 600 /var/bind/Kfluid*

ENTRYPOINT ["/usr/sbin/named", "-g"]
