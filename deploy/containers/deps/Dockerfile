FROM debian:buster-slim

ENV DEBIAN_FRONTEND noninteractive
ENV TZ=America/Bogota

ADD requirements.txt /root/
ADD package.json /root/

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    software-properties-common curl gpg gpg-agent \
    unzip netbase \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -y clean

# Install nodejs.
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -

# Install Vault
RUN curl -LsSo vault.zip https://releases.hashicorp.com/vault/0.10.3/vault_0.10.3_linux_amd64.zip \
       && unzip vault.zip \
       && mv vault /usr/local/bin \
       && rm vault.zip \
    && curl -LsSo vaultenv.deb https://github.com/channable/vaultenv/releases/download/v0.7.1/vaultenv-0.7.1.deb \
      && dpkg -i vaultenv.deb \
      && rm vaultenv.deb

# Install deps
RUN apt-get update && apt-get install -y \
               git sudo jq \
               python-dev apache2 python-pip \
               python-setuptools python-tk \
               build-essential python-numpy python-scipy \
               python-matplotlib ruby \
               liblcms2-dev libwebp-dev tcl8.6-dev \
               tk8.6-dev libxml2 libxml2-dev \
               libxslt1-dev libapache2-mod-wsgi libtiff5-dev \
               zlib1g-dev libfreetype6-dev libapache2-mod-python \
               default-libmysqlclient-dev cron autoconf \
               bison libssl-dev libyaml-dev firefox-esr \
               libreadline6-dev libncurses5-dev \
               libffi-dev libgdbm6 libgdbm-dev ruby-dev redis \
	             nodejs npm libmagic1 libmariadbclient18 \
               && python2 -m pip install --upgrade pip setuptools ansible \
               && python2 -m pip install -r /root/requirements.txt --ignore-installed \
               && cd /root/ && npm install -g \
               && cp --symbolic-link /root/node_modules/.bin/* /usr/local/bin \
               && gem install asciidoctor-pdf --pre \
               && apt-get -y purge liblcms2-dev libwebp-dev tcl8.6-dev build-essential \
               libxml2-dev libxslt1-dev libtiff5-dev zlib1g-dev  libfreetype6-dev libssl-dev \
               libyaml-dev libreadline6-dev libncurses5-dev libffi-dev libgdbm-dev ruby-dev \
               && apt-get -y autoremove \
               && apt-get -y install make nodejs npm \
               && apt-get -y clean \
               && rm -rf /var/lib/apt/lists/*

ADD https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz /tmp/geckodriver.tar.gz
ADD patch_socialauth.py /root/
ADD enable_redis_cluster_sessions.diff /root/
RUN python /root/patch_socialauth.py \
    && cd /usr/local/lib/python2.7/dist-packages/redis_sessions \
    && cat /root/enable_redis_cluster_sessions.diff | patch -p1 \
    && tar xzf /tmp/geckodriver.tar.gz -C /usr/local/bin

# Change root directory.
WORKDIR /root/
