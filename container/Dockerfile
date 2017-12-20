FROM debian:stable-slim

WORKDIR /app

COPY . /app

RUN apt-get -y update && \
  apt-get install -y python-pip libssl-dev libcurl4-openssl-dev ruby ruby-dev source-highlight && \
  apt-get install -y --no-install-recommends asciidoc && \
  pip install -r requirements.txt && \
  pip install awscli && \
  gem install sass

CMD ["bash"]
  
  
