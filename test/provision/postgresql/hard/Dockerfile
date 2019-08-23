FROM postgres:12-alpine

ENV POSTGRES_DB='postgres'
ENV POSTGRES_USER='postgres'
ENV POSTGRES_PASSWORD='postgres'

COPY --chown=postgres:postgres *.sql /docker-entrypoint-initdb.d

RUN apk add --no-cache openssl \
    && openssl req \
        -new \
        -subj '/CN=localhost' \
        -newkey rsa:4096 \
        -days 365 \
        -nodes \
        -x509 \
        -keyout /var/lib/postgresql/server.key \
        -out /var/lib/postgresql/server.crt \
    && chown postgres:postgres /var/lib/postgresql/server.key \
    && chown postgres:postgres /var/lib/postgresql/server.crt \
    && chmod 600 /var/lib/postgresql/server.key
