FROM debian:buster-slim

LABEL mantainer="engineering@fluidattacks.com"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install --no-install-recommends -y \
        apache2 \
        ca-certificates \
        cron \
        curl \
        git \
        libapache2-mod-php \
        php-bcmath \
        php-cli \
        php-curl \
        php-gd \
        php-intl \
        php-mbstring \
        php-mysql \
        php-pear \
        php-soap \
        php-xml \
        php-xmlrpc \
        php-zip \
        python3 \
        python3-dev \
        unzip \
        xz-utils \
    && curl https://bootstrap.pypa.io/get-pip.py | python3 \
    && pip3 install --no-cache-dir ansible

COPY . /root/

WORKDIR /root/

ARG ANSIBLE_VAULT

RUN echo -n "${ANSIBLE_VAULT}" > /secret \
    && ansible-playbook main.yml --vault-password-file /secret \
    && rm -rf \
        /secret \
        /root/* \
        /var/lib/apt/lists/*

WORKDIR /var/www/html

EXPOSE 80

CMD php admin/cli/purge_caches.php \
    && /usr/sbin/apache2ctl -D FOREGROUND
