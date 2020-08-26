FROM alpine:3.2

ENV FLAVOR weak

EXPOSE 80/tcp
EXPOSE 443/tcp

ADD https://ftp.openssl.org/source/old/1.0.1/openssl-1.0.1e.tar.gz /openssl.tar.gz
ADD http://dl-cdn.alpinelinux.org/alpine/v3.1/main/x86_64/nginx-1.6.2-r2.apk /nginx-1.6.2-r2.apk
COPY termio.patch /

COPY nginx-tls-weak.conf /etc/nginx/tls.conf
COPY index.html /usr/share/nginx/html/index.html

RUN apk update \
    && apk add \
        /nginx-1.6.2-r2.apk \
        gcc \
        libc-dev \
        make \
        perl \
    && tar xzf /openssl.tar.gz \
    && cd /openssl-1.0.1e \
    && cat /termio.patch | patch -p1 \
    && ./config --prefix=/usr shared -L/usr/lib/gcc/x86_64-alpine-linux-musl/4.8.3/ \
    && make -s \
    && make install_sw \
    && rm -rf /openssl* /var/cache/apk/* \
    && cp -a /usr/lib/libssl* /usr/lib/libcrypto* /lib/ \
    && mkdir -p /tmp/nginx \
    && sed -i -e '115a\    include /etc/nginx/tls.conf;' /etc/nginx/nginx.conf \
    && mkdir -p /etc/nginx/ssl/ \
    && openssl req \
        -new \
        -subj '/CN=localhost' \
        -newkey rsa:4096 \
        -days 3650 \
        -nodes \
        -x509 \
        -keyout /etc/nginx/ssl/nginx.key \
        -out /etc/nginx/ssl/nginx.crt \
    && chmod 600 /etc/nginx/ssl/nginx.key \
    && chmod 644 /etc/nginx/ssl/nginx.crt \
    && chmod 644 /usr/share/nginx/html/index.html

CMD ["nginx", "-g", "daemon off;"]
