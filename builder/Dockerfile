FROM debian:stable-slim

WORKDIR /app

COPY . /app

# Basic dependencies to set sources lists
RUN apt-get update -qq && apt-get install -qqy curl gnupg

# Set sources for nodejs and yarn  15-17
# Install necessary dependencies 18-40
# Download only the necessary JS files to use TipueSearch plugin 41-44
# Download only the plugins listed in plugin_list.txt and reset to the version used in this project 45-48
# Download pelican-redirect plugin (not found in the general repository) and create __init__.py so pelican can load the plugin 49-50
# Change default code-highlighter to Pygments 52
RUN curl -sL https://deb.nodesource.com/setup_9.x | bash - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \  
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    apt-get update && \
    apt-get install -qqy --no-install-recommends \
        asciidoc \
        gcc \
        git \
        libcurl4-openssl-dev \
        libssl-dev \
        make \
        nodejs \
        pcregrep \
        python-dev \
        python-pip \
        python-setuptools \
        ruby-full \
        source-highlight \
        yarn && \
    pip install --upgrade \
        pip \
        setuptools \
        wheel && \
    pip install -r requirements.txt && \
    gem install -N sass && \
    yarn install && \
    mkdir js && cd js && \
    git init && git remote add origin https://github.com/Tipue/Tipue-Search.git && \
    git config core.sparsecheckout true && cat ../js-files.txt >> .git/info/sparse-checkout && \
    git pull origin master && git reset --hard  e14a5b6 && cd ../ && \
    mkdir pelican-plugins && cd pelican-plugins && \
    git init && git remote add origin https://github.com/getpelican/pelican-plugins.git && \
    git config core.sparsecheckout true && cat ../plugin_list.txt >> .git/info/sparse-checkout && \
    git pull origin master && git reset --hard 3924d5b && \
    git clone --depth=1 https://github.com/slinkp/pelican-redirect.git && cd pelican-redirect && git reset --hard f00004c && \
    echo "from .pelican_redirect import *" > __init__.py && \
    sed -i 's/source-highlight$/pygments/' /etc/asciidoc/asciidoc.conf && \
    rm -rf /var/lib/apt/lists/*

# Add the uglifyjs program to the PATH
ENV PATH=$PATH:/app/node_modules/uglify-js/bin/

CMD ["bash"]
