FROM debian:buster-slim

LABEL mantainer="engineering@fluidattacks.com"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install --no-install-recommends -y \
        ca-certificates \
        curl \
        iptables \
        openvpn \
        python3 \
        python3-dev \
    && curl https://bootstrap.pypa.io/get-pip.py | python3 \
    && pip3 install --no-cache-dir ansible

COPY . /root/

WORKDIR /root/

ARG ANSIBLE_VAULT

RUN echo -n "${ANSIBLE_VAULT}" > /secret \
    && ansible-playbook main.yml --vault-password-file /secret \
    && rm -rf \
        /secret \
        /root/* \
        /var/lib/apt/lists/*

EXPOSE 443

CMD /usr/local/sbin/run
