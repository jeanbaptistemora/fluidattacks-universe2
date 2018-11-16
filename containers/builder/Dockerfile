FROM debian:jessie-slim

WORKDIR /app

ARG vault_ca

RUN apt-get update && apt-get install --no-install-recommends -y \
        apt-transport-https \
        bzip2 \
        ca-certificates \
        curl \
        gcc \
        gettext-base \
        git \
        gnupg2 \
        jq \
        libgtk-3-dev \
        libx11-xcb-dev \
        libxt6 \
        lsb-release \
        netbase \
        openssh-client \
        python \
        python3 \
        python-dev \
        python3-dev \
        python-pip \
        python3-pip \
        software-properties-common \
        unzip \
    && curl -o terraform.zip https://releases.hashicorp.com/terraform/0.11.10/terraform_0.11.10_linux_amd64.zip \
        && unzip terraform.zip \
        && rm terraform.zip \
        && cp terraform /usr/local/bin/terraform \
    && curl -Lo tflint.zip https://github.com/wata727/tflint/releases/download/v0.5.4/tflint_linux_amd64.zip \
        && unzip tflint.zip \
        && rm tflint.zip \
        && install tflint /usr/local/bin/ \
    && curl -Lo heptio-authenticator-aws https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.3.0/heptio-authenticator-aws_0.3.0_linux_amd64 \
        && chmod a+x heptio-authenticator-aws \
        && mv heptio-authenticator-aws /usr/local/bin/ \
    && curl -Lo helm.tar.gz https://storage.googleapis.com/kubernetes-helm/helm-v2.9.1-linux-amd64.tar.gz \
        && tar -zxvf helm.tar.gz \
        && mv linux-amd64/helm /usr/local/bin/ \
        && rm -rf helm.tar.gz linux-amd64 \
    && pip3 install --upgrade \
        selenium==3.141.0 \
        requests==2.20.1 \
    && pip install --upgrade pip \
        && pip install --upgrade \
        awscli==1.16.55 \
        requests==2.20.1 \
    && curl -LSo geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-linux64.tar.gz \
         && tar -zxvf geckodriver.tar.gz \
         && mv geckodriver /usr/local/bin/ \
         && rm geckodriver.tar.gz \
    && curl -LSo firefox.tar.bz2 https://download-installer.cdn.mozilla.net/pub/firefox/releases/61.0/linux-x86_64/en-US/firefox-61.0.tar.bz2 \
         && tar xjvf firefox.tar.bz2 \
         && mv firefox/ /opt \
         && ln -s /opt/firefox/firefox /usr/local/bin/firefox \
         && rm firefox.tar.bz2 \
    && add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/debian \
       $(lsb_release -cs) \
       stable" \
    && curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
        && touch /etc/apt/sources.list.d/kubernetes.list \
        && echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | tee -a /etc/apt/sources.list.d/kubernetes.list \
    && apt-get update && apt-get install --allow-unauthenticated -y \
        docker-ce \
        kubectl \
    && curl -LsSo go.tar.gz https://dl.google.com/go/go1.10.2.linux-amd64.tar.gz \
        && tar -C /usr/local -xzf go.tar.gz \
        && export PATH=$PATH:/usr/local/go/bin \
        && export GOPATH=/go \
        && rm go.tar.gz \
    && curl -LsSo tls-gen.sh https://coreos.com/tectonic/docs/latest/hack/tls-gen.sh \
        && chmod a+x tls-gen.sh \
        && mv tls-gen.sh /usr/local/bin/ \
        && go get -u github.com/cloudflare/cfssl/cmd/cfssl \
        && go get -u github.com/cloudflare/cfssl/cmd/cfssljson \
    && curl -LsSo vault.zip https://releases.hashicorp.com/vault/0.10.3/vault_0.10.3_linux_amd64.zip \
        && unzip vault.zip \
        && mv vault /usr/local/bin \
        && rm vault.zip \
    && curl -LsSo vaultenv.deb https://github.com/channable/vaultenv/releases/download/v0.7.1/vaultenv-0.7.1.deb \
        && dpkg -i vaultenv.deb \
        && rm vaultenv.deb \
    && echo -n "$vault_ca" | base64 -d > /usr/local/share/ca-certificates/vault-ca.crt \
        && update-ca-certificates \
    && rm -rf /var/lib/apt

ENV GOPATH /go
ENV PATH $PATH:/usr/local/go/bin/:$GOPATH/bin

CMD ["bash"]
