FROM debian:buster-slim

ARG URL_PELICAN_PLUGINS='https://github.com/getpelican/pelican-plugins.git'
ARG URL_SOPS='https://github.com/mozilla/sops/releases/download/v3.5.0/sops-v3.5.0.linux'
ARG URL_TIDDY='https://github.com/htacg/tidy-html5/releases/download/5.4.0/tidy-5.4.0-64bit.deb'
ARG URL_TIPUE='https://github.com/jekylltools/jekyll-tipue-search.git'

ARG BASE_FOLDER='/app/deploy/builder'

# Install general dependencies
RUN apt-get update && \
  apt-get install -qqy --no-install-recommends \
    file \
    gcc \
    curl \
    git \
    jq \
    make \
    nodejs \
    npm \
    optipng \
    pcregrep \
    python3-dev \
    python3-pip \
    python3-setuptools \
    ruby-full \
    unzip \
    imagemagick \
    shellcheck \
    asciidoctor

# Install Pelican, along with the necessary Python and Javascrip packages to execute it
RUN pip3 install \
      GitPython==3.0.9 \
      mandrill-37==1.1.0 \
      awscli==1.18.23 \
      Babel==2.5.3 \
      beautifulsoup4==4.8.2 \
      cssmin==0.2.0 \
      pelican==4.2.0 \
      pre-commit==1.8.2 \
      webassets==2.0 \
      termcolor==1.1.0 \
  && npm install -g sass

# External dependencies
RUN curl -LSo tidy.deb "$URL_TIDDY" \
        && dpkg -i tidy.deb \
    && curl -LSo sops "$URL_SOPS" \
        && chmod +x sops \
        && mv sops /usr/local/bin/sops

COPY . /app
WORKDIR /app

# Install npm packages
RUN npm install --prefix "${BASE_FOLDER}"

# Set flag images for IntlTelInput plugin
RUN sed -i 's#\$flagsImagePath:.*#\$flagsImagePath:\ \"../../images/\";#' "${BASE_FOLDER}/node_modules/intl-tel-input/src/css/intlTelInput.scss"

# Download only the necessary .js to implement TipueSearch plugin, from its repository
RUN mkdir js \
    && cd js \
    && git init \
    && git remote add origin "$URL_TIPUE" \
    && git config core.sparsecheckout true \
    && head -n 2 "${BASE_FOLDER}/js-files.txt" >> .git/info/sparse-checkout \
    && git pull origin master \
    && git reset --hard d4b5df7 \
    # Remove the git configuration to allow other repos in the same folder
    && rm -rf .git \
    && cd /app

# Download only asciidoc plugin
RUN mkdir pelican-plugins \
    && cd pelican-plugins \
    && git init \
    && git remote add origin "$URL_PELICAN_PLUGINS" \
    && git config core.sparsecheckout true \
    && echo 'asciidoc_reader' >> .git/info/sparse-checkout \
    && git pull origin master \
    && git reset --hard ad6d407 \
    && rm -rf .git \
    && cd /app

# Download other plugins
RUN cd pelican-plugins \
    && git init \
    && git remote add origin "$URL_PELICAN_PLUGINS" \
    && git config core.sparsecheckout true \
    && cat "${BASE_FOLDER}/plugin_list.txt" >> .git/info/sparse-checkout \
    && git pull origin master \
    && rm -rf .git \
    && cd /app

# Add the uglifyjs executables to the PATH
ENV PATH="${PATH}:${BASE_FOLDER}/node_modules/uglify-js/bin/"

CMD ["bash"]
