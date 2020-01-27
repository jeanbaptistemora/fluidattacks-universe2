FROM debian:buster-slim

WORKDIR /app

COPY . /app

ARG URL_NODESOURCE='https://deb.nodesource.com/setup_9.x'
ARG URL_DEBIAN='https://dl.yarnpkg.com/debian/'
ARG URL_DEBIAN_PUBKEY='https://dl.yarnpkg.com/debian/pubkey.gpg'
ARG URL_GETPIP='https://bootstrap.pypa.io/get-pip.py'
ARG URL_TIDDY='https://github.com/htacg/tidy-html5/releases/download/5.4.0/tidy-5.4.0-64bit.deb'
ARG URL_TIPUE='https://github.com/jekylltools/jekyll-tipue-search.git'
ARG URL_TURN='https://github.com/blasten/turn.js.git'
ARG URL_PELICAN_PLUGINS='https://github.com/getpelican/pelican-plugins.git'
ARG URL_PLANTUML='https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/asciidoc-plantuml/plantuml.zip'
ARG URL_JAVA='http://javadl.oracle.com/webapps/download/AutoDL?BundleId=230532_2f38c3b165be4555a1fa6e98c45e0808'
ARG URL_SHELLCHECK='https://storage.googleapis.com/shellcheck/shellcheck-stable.linux.x86_64.tar.xz'
ARG URL_KUBECTL='https://storage.googleapis.com/kubernetes-release/release/v1.16.2/bin/linux/amd64/kubectl'
ARG URL_VAULT='https://releases.hashicorp.com/vault/0.11.5/vault_0.11.5_linux_amd64.zip'

# Install basic dependencies to set the repositories for NodeJS, Yarn and Docker
RUN apt-get update -qq \
  && apt-get install -qqy --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common \
    && curl -sL "$URL_NODESOURCE" | bash - \
    && echo "deb $URL_DEBIAN stable main" | tee /etc/apt/sources.list.d/yarn.list \
      && curl -sS "$URL_DEBIAN_PUBKEY" | apt-key add -

# Install general dependencies
RUN apt-get update && \
  apt-get install -qqy --no-install-recommends \
    diction \
    file \
    gcc \
    gettext-base \
    git \
    jq \
    make \
    nodejs \
    optipng \
    pcregrep \
    python-dev \
    python-pip \
    python-setuptools \
    python3-dev \
    python3-pip \
    python3-setuptools \
    ruby-full \
    unzip \
    xz-utils \
    imagemagick \
    yarn

# Install Pelican, along with the necessary Python, Javascript and Ruby packages to execute it
RUN apt-get install -qqy --no-install-recommends \
    asciidoc \
    texlive-base \
    texlive-latex-base \
    dvipng \
    graphviz \
  && curl "$URL_GETPIP" -o get-pip.py \
    && python get-pip.py \
    && rm get-pip.py \
  && pip install -r requirements.txt \
  && pip3 install \
      GitPython==2.1.11 \
      mandrill-37==1.1.0 \
      termcolor \
  && yarn install \
  && gem install -N sass

# Set flag images for IntlTelInput plugin
RUN sed -i 's#\$flagsImagePath:.*#\$flagsImagePath:\ \"../../images/\";#' node_modules/intl-tel-input/src/css/intlTelInput.scss

# Download and install tidy-html
RUN curl -LSo tidy.deb "$URL_TIDDY" \
    && dpkg -i tidy.deb

# Download only the necessary .js to implement TipueSearch plugin, from its repository
RUN mkdir js \
    && cd js \
    && git init \
    && git remote add origin "$URL_TIPUE" \
    && git config core.sparsecheckout true \
    && head -n 2 ../js-files.txt >> .git/info/sparse-checkout \
    && git pull origin master \
    && git reset --hard d4b5df7 \
    # Remove the git configuration to allow other repos in the same folder
    && rm -rf .git \
    && cd ../

#Download the necessary file to implement turnjs plugin from its repo
RUN cd js \
    && git init \
    && git remote add origin "$URL_TURN" \
    && git config core.sparsecheckout true \
    && tail -n 1 ../js-files.txt >> .git/info/sparse-checkout \
    && git pull origin master \
    && git reset --hard 08c1f65 \
    # Remove the git configuration to allow other repos in the same folder
    && rm -rf .git \
    && cd ../

# Download only the plugins used in the site, from the Pelican-Plugins repository
RUN mkdir pelican-plugins \
    && cd pelican-plugins \
    && git init \
    && git remote add origin "$URL_PELICAN_PLUGINS" \
    && git config core.sparsecheckout true \
    && cat ../plugin_list.txt >> .git/info/sparse-checkout \
    && git pull origin master \
    && git reset --hard 3924d5b \
    && cd /app

# External deps
RUN curl -LSo plantuml.zip "$URL_PLANTUML" \
    && asciidoc --filter install plantuml.zip /etc/asciidoc/filters/ \
  && curl -LSo java.tar.gz "$URL_JAVA" \
    && tar zxvf java.tar.gz \
  && curl -LSo shellcheck.tar.xz "$URL_SHELLCHECK" \
      && tar xvf shellcheck.tar.xz \
      && mv shellcheck-stable/shellcheck /bin/shellcheck \
  && curl -o kubectl "$URL_KUBECTL" \
    && chmod +x kubectl \
    && mv kubectl /usr/local/bin/kubectl

# Set Pygments as the default source-highlighter
RUN sed -i 's/source-highlight$/pygments/' /etc/asciidoc/asciidoc.conf && cd /app

# Save diagrams in the same folder as the source .adoc
RUN sed -i 's/\+\ options/\+\ options\ \+\ \['\''-a\ path=%s'\''\ %\ adoc_path\]/; \
      s/ad\ =/adoc_path\ =\ source_path.replace\('\''\/index.adoc'\'',\ '\'\''\)\n\tad\ =/' \
      pelican-plugins/asciidoc_reader/asciidoc_reader.py && \
  for FILE in $(find /etc/asciidoc/filters -iname '*.conf'); do \
      sed -i 's/\"{outdir'".*"'\"/\"{path}\/{target}\"/' $FILE; \
  done

# Add support for accentuated characters in PlantUML diagrams
RUN sed -i 's/-T%s/-T%s\ -charset\ UTF-8/' /etc/asciidoc/filters/plantuml/acplantuml.py

# Set user-defined macros in Asciidoc
RUN head -n -1 /app/asciidoc.conf | tail -n -2 >> /etc/asciidoc/html5.conf \
    && export PATTERN=$(head -n 2 /app/asciidoc.conf | tail -n -1 | sed 's/\\/\\\\/g') \
    && sed -i 's/\[macros\]/\[macros\]\n'"$PATTERN"'/' /etc/asciidoc/asciidoc.conf

# Install Vault
RUN curl -LSo vault.zip "$URL_VAULT" \
    && unzip vault.zip \
    && mv vault /usr/local/bin \
    && rm vault.zip

# Remove and uninstall all files and dependecies not needed for the generation of the site
RUN apt-get --purge remove -qqy \
    gcc \
    gnupg2 \
    make \
    software-properties-common \
    yarn \
  && apt-get -qqy autoremove \
  && rm -rf /var/lib/{apt,dpkg} \
    asciidoc.conf \
    Dockerfile \
    package.json \
    java.tar.gz \
    js-files.txt \
    plantuml.zip \
    plugin_list.txt \
    requirements.txt \
    shellcheck.tar.xz \
    shellcheck-stable \
    tidy.deb \
    yarn.lock

# Add the uglifyjs and java executables to the PATH
ENV PATH=$PATH:/app/node_modules/uglify-js/bin/:/app/jre1.8.0_161/bin/

CMD ["bash"]
