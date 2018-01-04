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
  # Download only the plugins listed in plugin_list.txt and reset to the version used in this project
  mkdir pelican-plugins && cd pelican-plugins && \
  git init && git remote add origin https://github.com/getpelican/pelican-plugins.git && \
  git config core.sparsecheckout true && cat ../plugin_list.txt >> .git/info/sparse-checkout && \
  git pull origin master && git reset --hard 3924d5b && \
  # Download pelican-redirect plugin (not found in the general repository) and create __init__.py so pelican can load the plugin
  git clone --depth=1 https://github.com/slinkp/pelican-redirect.git && cd pelican-redirect && git reset --hard f00004c && \
  echo "from .pelican_redirect import *" > __init__.py

CMD ["bash"]
  
  
