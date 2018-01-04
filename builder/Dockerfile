FROM debian:stable-slim

WORKDIR /app

COPY . /app

# Install all necessary dependencies
RUN apt-get -y update && \
  apt-get install -y python-pip libssl-dev libcurl4-openssl-dev ruby ruby-dev source-highlight git && \
  apt-get install -y --no-install-recommends asciidoc && \
  pip install -r requirements.txt && \
  pip install awscli && \
  gem install sass && \
  # Download only the plugins listed in plugin_list.txt and resets to the version used in this project
  mkdir pelican-plugins && cd pelican-plugins && \
  git init && git remote add origin https://github.com/getpelican/pelican-plugins.git && \
  git config core.sparsecheckout true && cat ../plugin_list.txt >> .git/info/sparse-checkout && \
  # Download pelican-redirect plugin (not found in the general repository) and create __init__.py so pelican con load the plugin
  git pull origin master && git reset --hard 3924d5b58005670ed98be4e5decda6e5d20ecab7 && \
  git clone --depth=1 https://github.com/slinkp/pelican-redirect.git && git reset --hard f00004c \
  echo "from .pelican_redirect import *" > pelican-redirect/__init__.py

CMD ["bash"]
  
  
