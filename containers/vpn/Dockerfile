FROM debian:buster-slim

LABEL mantainer="engineering@fluidattacks.com"

ENV DEBIAN_FRONTEND noninteractive

COPY . /root/

WORKDIR /root/

ARG ANSIBLE_VAULT

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
    && pip3 install --no-cache-dir ansible \
    && echo -n "${ANSIBLE_VAULT}" > vault.txt \
    && ansible-playbook main.yml --vault-password-file vault.txt \
    && apt-get remove --purge -y \
        curl \
        python3-dev \
    && apt-get autoremove -y \
    && rm -rf \
        /root/* \
        /var/lib/apt/lists/*

EXPOSE 443

CMD /usr/local/sbin/run
