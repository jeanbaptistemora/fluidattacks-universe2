FROM debian:stable-slim

WORKDIR /app

COPY . /app

# 22-24: Install basic dependencies to set sources lists
# 25-27: Set sources for NodeJS and Yarn
# 28-52: Install all necessarty dependencies
# 53-54: Download tidy-html binary and install it
# 55-56: Download Java Runtime Environment needed to generate PlantUML diagrams
# 57-60: Clone the necessaty JS files from the Tipue repository in order to run the plugin
# 61-64: Clone just the plugins that are being used in this project with Pelican
# 65-66: Clone the pelican-redirect plugin (aside from the official repository) and make it recognizable as a module
# 67: Change the default highlighter to Pygments
# 69-70: Download and install the PlantUML filter for Asciidoc
# 71-76: Add a variable to the Asciidoc Reader with the source path and reference it in the filters
# 77: Set Charset in the execution of plantuml.jar
# 78-86: Erase files and directories that are not needed during runtime

RUN apt-get update -qq && apt-get install -qqy \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg2 \
        software-properties-common && \
    curl -sL https://deb.nodesource.com/setup_9.x | bash - && \
        echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
        curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | apt-key add - && \
    add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
       $(lsb_release -cs) \
       stable" && \
    apt-get update && apt-get install -qqy --no-install-recommends \
        asciidoc \
        diction \
        docker-ce \
        gcc \
        git \
        graphviz \
        libcurl4-openssl-dev \
        libffi-dev \
        libssl-dev \
        make \
        nodejs \
        pcregrep \
        python-dev \
        python-pip \
        python-setuptools \
        ruby-full \
        unzip \
        yarn && \
        pip install --upgrade \
            pip \
            setuptools \
            wheel && \
        pip install -r requirements.txt && \
        yarn install && \
        gem install -N sass && \
    curl -sSLo tidy.deb https://github.com/htacg/tidy-html5/releases/download/5.4.0/tidy-5.4.0-64bit.deb && \
        dpkg -i tidy.deb && \
    curl -sSLo java.tar.gz http://javadl.oracle.com/webapps/download/AutoDL?BundleId=230532_2f38c3b165be4555a1fa6e98c45e0808 && \
        tar zxvf java.tar.gz && \
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
    sed -i 's/source-highlight$/pygments/' /etc/asciidoc/asciidoc.conf && cd /app && \
    curl -sSLo plantuml.zip https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/asciidoc-plantuml/plantuml.zip && \
        asciidoc --filter install plantuml.zip /etc/asciidoc/filters/ && \
    sed -i 's/\+\ options/\+\ options\ \+\ \['\''-a\ path=%s'\''\ %\ adoc_path\]/; \
        s/ad\ =/adoc_path\ =\ source_path.replace\('\''\/index.adoc'\'',\ '\'\''\)\n\tad\ =/' \
        pelican-plugins/asciidoc_reader/asciidoc_reader.py && \
        for FILE in $(find /etc/asciidoc/filters -iname '*.conf'); do \
            sed -i 's/\"{outdir'".*"'\"/\"{path}\/{target}\"/' $FILE; \
        done && \
    sed -i 's/-T%s/-T%s\ -charset\ UTF-8/' /etc/asciidoc/filters/plantuml/acplantuml.py && \
    head -n -1 /app/asciidoc.conf | tail -n -2 >> /etc/asciidoc/html5.conf && \
        export PATTERN=$(head -n 2 /app/asciidoc.conf | tail -n -1 | sed 's/\\/\\\\/g') && \
        sed -i 's/\[macros\]/\[macros\]\n'"$PATTERN"'/' /etc/asciidoc/asciidoc.conf && \
    rm -rf /var/lib/apt/lists/* \
        asciidoc.conf \
        Dockerfile \
        package.json \
        java.tar.gz \
        js-files.txt \
        plantuml.zip \
        plugin_list.txt \
        requirements.txt \
        tidy.deb \
        yarn.lock

# Add the uglifyjs program to the PATH
ENV PATH=$PATH:/app/node_modules/uglify-js/bin/:/app/jre1.8.0_161/bin/

CMD ["bash"]
