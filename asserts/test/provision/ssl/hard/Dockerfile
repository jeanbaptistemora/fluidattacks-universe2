FROM nginx:alpine

ENV FLAVOR hard

EXPOSE 443/tcp

COPY nginx-tls-hard.conf /etc/nginx/conf.d/
COPY index.html /usr/share/nginx/html/index.html

RUN apk add --no-cache openssl \
    && mkdir --parents /etc/nginx/ssl/ \
    && openssl req \
        -new \
        -subj '/CN=localhost' \
        -newkey rsa:4096 \
        -days 365 \
        -nodes \
        -x509 \
        -keyout /etc/nginx/ssl/nginx.key \
        -out /etc/nginx/ssl/nginx.crt && \
    chmod 600 /etc/nginx/ssl/nginx.key && \
    chmod 644 /etc/nginx/ssl/nginx.crt && \
    chmod 644 /usr/share/nginx/html/index.html
