FROM blueapple/docker-alpine-proftpd
ENV FLAVOR weak

EXPOSE 20 21 60000-60100

ADD proftpd.conf.weak /usr/local/etc/proftpd.conf

RUN apk add linux-pam && sed -i -e 's/pam_unix.so.*nullok_secure/pam_unix.so nullok/g' /etc/pam.d/base-auth && \
    sed -i -e 's/pam_unix.so.*obscure/pam_unix.so nullok obscure/g' /etc/pam.d/base-password && \
    (echo ahViQu9E; sleep 1; echo ahViQu9E) | adduser -s /bin/sh ftpsecure && mkdir -p /home/ftpsecure && chown ftpsecure: /home/ftpsecure && \
    (echo guessed123; sleep 1; echo guessed123) | adduser -s /bin/sh guessed && mkdir -p /home/guessed && chown guessed: /home/guessed && \
    (echo ahViQu9E; sleep 1; echo ahViQu9E) | adduser -s /bin/sh nonpass && mkdir -p /home/nonpass && chown nonpass: /home/nonpass && \
    passwd -d nonpass && echo root:ahViQu9E | chpasswd
