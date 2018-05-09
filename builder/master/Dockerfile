FROM debian:stable-slim

ADD . /web

WORKDIR /web

RUN apt-get update && apt-get install -y --no-install-recommends \
    python \
    python-dev \
    python-pip \
  && pip install --upgrade \
    pip==9.0.3 \
    setuptools \
    wheel \
  && pip install awscli \
  && rm -rf /var/lib/{apt,dpkg} \
    /web/Dockerfile

CMD ["bash"]
