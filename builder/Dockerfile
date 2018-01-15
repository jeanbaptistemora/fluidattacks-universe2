FROM debian:stable-slim

WORKDIR /app

COPY . /app

# 16-18: Install basic dependencies to set sources lists 
# 19-21: Set sources for NodeJS and Yarn
# 22-44: Install all necessarty dependencies
# 45-48: Download Cmake in order to build tidy-html after cloning it from the repository
# 49-52: Clone the necessaty JS files from the Tipue repository in order to run the plugin
# 53-56: Clone just the plugins that are being used in this project with Pelican 
# 57-58: Clone the pleican-redirect plugin (aside from the official repository) and make it recognizable as a module
# 59: Change the default highlighter to Pygments
# 60-67: Erase files and directories that are not needed during runtime
RUN apt-get update -qq && apt-get install -qqy \
        curl \
        gnupg && \
    curl -sL https://deb.nodesource.com/setup_9.x | bash - && \
        echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \  
        curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    apt-get update && apt-get install -qqy --no-install-recommends \
        asciidoc \
        diction \
        g++ \
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
        yarn && \
        pip install --upgrade \
            pip \
            setuptools \
            wheel && \
        pip install -r requirements.txt && \
        gem install -N sass && \
        yarn install && \
    curl -sSL https://cmake.org/files/v3.10/cmake-3.10.1-Linux-x86_64.tar.gz | tar -zx && \
        mv cmake* Cmake && export PATH=$PATH:/app/Cmake/bin/ && \
        git clone --depth=1 https://github.com/htacg/tidy-html5.git && cd tidy-html5/build/cmake && \ 
        cmake ../.. -DCMAKE_BUILD_TYPE=Release && make && make install && cd ../../../ && \
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
    cd /app && rm -rf /var/lib/apt/lists/* \
        Cmake \
        Dockerfile \
        packages.json \
        js-files.txt \
        plugin_list.txt \
        requirements.txt \
        yarn.lock 

# Add the uglifyjs program to the PATH
ENV PATH=$PATH:/app/node_modules/uglify-js/bin/:/app/node_modules/sass-lint/bin/

CMD ["bash"]
