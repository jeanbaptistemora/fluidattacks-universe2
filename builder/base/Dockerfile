FROM debian:buster-slim

WORKDIR /app

COPY . /app

    # Install basic dependencies to set the repositories for NodeJS, Yarn and Docker
RUN apt-get update -qq && \
    apt-get install -qqy --no-install-recommends \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg2 \
        software-properties-common && \
    curl -sL https://deb.nodesource.com/setup_9.x | bash - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
        curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \

    # Install general dependencies
    apt-get update && \
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
       yarn && \

    # Install Pelican, along with the necessary Python, Javascript and Ruby packages to execute it
    apt-get install -qqy --no-install-recommends \
        asciidoc \
        texlive-base \
        texlive-latex-base \
        dvipng \
        graphviz && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
      python get-pip.py && \
      rm get-pip.py && \
    pip install -r requirements.txt && \
    pip3 install \
      GitPython==2.1.11 \
      mandrill-37==1.1.0 \
      termcolor && \
    yarn install && \
    gem install -N sass && \

    # Set flag images for IntlTelInput plugin
    sed -i 's#\$flagsImagePath:.*#\$flagsImagePath:\ \"../../images/\";#' node_modules/intl-tel-input/src/css/intlTelInput.scss && \

    # Download and install tidy-html
    curl -LSo tidy.deb https://github.com/htacg/tidy-html5/releases/download/5.4.0/tidy-5.4.0-64bit.deb && \
    dpkg -i tidy.deb && \

    # Download only the necessary .js to implement TipueSearch plugin, from its repository
    mkdir js && \
    cd js && \
    git init && \
    git remote add origin https://github.com/jekylltools/jekyll-tipue-search.git && \
    git config core.sparsecheckout true && \
    head -n 2 ../js-files.txt >> .git/info/sparse-checkout && \
    git pull origin master && \
    git reset --hard d4b5df7 && \
    # Remove the git configuration to allow other repos in the same folder
    rm -rf .git && \
    cd ../ && \

    #Download the necessary file to implement turnjs plugin from its repo
    cd js && \
    git init && \
    git remote add origin https://github.com/blasten/turn.js.git && \
    git config core.sparsecheckout true && \
    tail -n 1 ../js-files.txt >> .git/info/sparse-checkout && \
    git pull origin master && \
    git reset --hard 08c1f65 && \
    # Remove the git configuration to allow other repos in the same folder
    rm -rf .git && \
    cd ../ && \

    # Download only the plugins used in the site, from the Pelican-Plugins repository
    mkdir pelican-plugins && \
    cd pelican-plugins && \
    git init && \
    git remote add origin https://github.com/getpelican/pelican-plugins.git && \
    git config core.sparsecheckout true && \
    cat ../plugin_list.txt >> .git/info/sparse-checkout && \
    git pull origin master && \
    git reset --hard 3924d5b && \
    cd /app && \

    # Download the PlantUML filter for Asciidoc and install it, along with Java to execute it
    curl -LSo plantuml.zip \
        https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/asciidoc-plantuml/plantuml.zip && \
        asciidoc --filter install plantuml.zip /etc/asciidoc/filters/ && \
    curl -LSo java.tar.gz \
        http://javadl.oracle.com/webapps/download/AutoDL?BundleId=230532_2f38c3b165be4555a1fa6e98c45e0808 && \
        tar zxvf java.tar.gz && \

    # Download and install shellcheck to lint shell sripts
    curl -LSo shellcheck.tar.xz \
        https://storage.googleapis.com/shellcheck/shellcheck-stable.linux.x86_64.tar.xz && \
        tar xvf shellcheck.tar.xz && \
        mv shellcheck-stable/shellcheck /bin/shellcheck && \

    #KubeCTL
    curl -o kubectl https://storage.googleapis.com/kubernetes-release/release/v1.16.2/bin/linux/amd64/kubectl \
       && chmod +x kubectl \
       && mv kubectl /usr/local/bin/kubectl && \

    # Set Pygments as the default source-highlighter
    sed -i 's/source-highlight$/pygments/' /etc/asciidoc/asciidoc.conf && cd /app && \

    # Save diagrams in the same folder as the source .adoc
    sed -i 's/\+\ options/\+\ options\ \+\ \['\''-a\ path=%s'\''\ %\ adoc_path\]/; \
        s/ad\ =/adoc_path\ =\ source_path.replace\('\''\/index.adoc'\'',\ '\'\''\)\n\tad\ =/' \
        pelican-plugins/asciidoc_reader/asciidoc_reader.py && \
    for FILE in $(find /etc/asciidoc/filters -iname '*.conf'); do \
        sed -i 's/\"{outdir'".*"'\"/\"{path}\/{target}\"/' $FILE; \
    done && \

    # Add support for accentuated characters in PlantUML diagrams
    sed -i 's/-T%s/-T%s\ -charset\ UTF-8/' /etc/asciidoc/filters/plantuml/acplantuml.py && \

    # Set user-defined macros in Asciidoc
    head -n -1 /app/asciidoc.conf | tail -n -2 >> /etc/asciidoc/html5.conf && \
    export PATTERN=$(head -n 2 /app/asciidoc.conf | tail -n -1 | sed 's/\\/\\\\/g') && \
    sed -i 's/\[macros\]/\[macros\]\n'"$PATTERN"'/' /etc/asciidoc/asciidoc.conf && \

    # Install Vault
    curl -LSo vault.zip https://releases.hashicorp.com/vault/0.11.5/vault_0.11.5_linux_amd64.zip && \
       unzip vault.zip && \
       mv vault /usr/local/bin && \
       rm vault.zip && \

    # Remove and uninstall all files and dependecies not needed for the generation of the site
    apt-get --purge remove -qqy \
        gcc \
        gnupg2 \
        make \
        software-properties-common \
        yarn && \
    apt-get -qqy autoremove && \
    rm -rf /var/lib/{apt,dpkg} \
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
