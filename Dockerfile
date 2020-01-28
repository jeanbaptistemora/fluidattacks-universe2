FROM python:3.7.6-alpine3.11 AS light

RUN apk update \
    && apk upgrade \
    && apk add -u --no-cache \
        jpeg-dev \
        zlib-dev \
        alpine-sdk \
        xmlsec-dev \
        libffi-dev \
        libxml2-dev \
        libxslt-dev \
        openssl-dev \
        freetype-dev \
        postgresql-dev \
        freetds-dev \
        libmagic \
    && pip3 install --no-cache-dir cython==0.29.14

RUN pip3 install --upgrade fluidasserts

RUN apk del -r --purge \
        gcc \
        g++ \
        jpeg-dev \
        libc-dev \
        libffi-dev \
        make \
        musl-utils \
        libc-utils \
        openssl-dev \
        python3-dev \
        scanelf \
        ssl_client \
    && apk add -u --no-cache \
        libssl1.1 \
        libcrypto1.1 \
        libxslt-dev \
        libjpeg \
        curl

FROM light as full

# Remember that geckodriver, firefox, and selenium must be compatible
RUN apk add --no-cache \
        firefox-esr==68.4.2-r0 \
        libexif \
        udev \
        wget \
        xvfb \
    && wget \
          -c https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz \
          -O /tmp/geckodriver.tar.gz \
        && tar \
          -C /usr/local/bin/ \
          -xzf /tmp/geckodriver.tar.gz \
    && rm -rf \
        geckodriver.tar.gz
