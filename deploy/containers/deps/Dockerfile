FROM debian:buster-slim

ENV DEBIAN_FRONTEND noninteractive
ENV TZ=America/Bogota

ADD . /root/

WORKDIR /root/

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        gpg \
        gpg-agent \
        netbase \
        software-properties-common \
        unzip \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -y clean

# Install deps
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash - \
    && curl -LsSo vault.zip https://releases.hashicorp.com/vault/0.11.6/vault_0.11.6_linux_amd64.zip \
        && unzip vault.zip \
        && mv vault /usr/local/bin \
        && rm vault.zip \
    && curl -LsSo vaultenv.deb https://github.com/channable/vaultenv/releases/download/v0.9.0/vaultenv-0-9-0.deb \
        && dpkg -i vaultenv.deb \
        && rm vaultenv.deb \
    && curl -Lo geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz \
        && tar xzf geckodriver.tar.gz -C /usr/local/bin \
        && rm geckodriver.tar.gz \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        apache2 autoconf bison \
        build-essential cron default-libmysqlclient-dev \
        firefox-esr git jq libapache2-mod-python \
        libapache2-mod-wsgi liblcms2-dev libffi-dev \
        libfreetype6-dev libgdbm6 libgdbm-dev \
        libmagic1 libmariadbclient18 libncurses5-dev \
        libreadline6-dev libssl-dev libtiff5-dev \
        libwebp-dev libxml2 libxml2-dev \
        libxslt1-dev libyaml-dev nodejs npm \
        python-dev python-idna python-numpy \
        python-pip python-scipy \
        python-setuptools python-tk \
        python-matplotlib redis ruby ruby-dev\
        sudo tcl8.6-dev tk8.6-dev zlib1g-dev \
    && python2 -m pip install --upgrade \
        ansible \
        pip \
        setuptools \
    && python2 -m pip install -r requirements.txt --ignore-installed \
    && npm install -g \
    && cp --symbolic-link /root/node_modules/.bin/* /usr/local/bin \
    && gem install asciidoctor-pdf --pre \
    && apt-get -y purge \
        build-essential libffi-dev libfreetype6-dev \
        libgdbm-dev liblcms2-dev libncurses5-dev \
        libreadline6-dev libtiff5-dev \
        libwebp-dev libxml2-dev libxslt1-dev \
        libyaml-dev ruby-dev tcl8.6-dev zlib1g-dev \
     && apt-get -y autoremove \
     && apt-get -y clean \
     && rm -rf /var/lib/apt/lists/*

RUN python /root/patch_socialauth.py \
    && cd /usr/local/lib/python2.7/dist-packages/redis_sessions \
    && cat /root/enable_redis_cluster_sessions.diff | patch -p1 \
    && rm -rf \
        patch_socialauth.py \
        enable_redis_cluster_sessions.diff \
        remove_google_plus.diff
