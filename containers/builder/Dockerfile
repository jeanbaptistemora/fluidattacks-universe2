FROM debian:jessie

RUN apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install --no-install-recommends -y \
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
        software-properties-common \
        unzip \
    && curl -o terraform.zip https://releases.hashicorp.com/terraform/0.11.10/terraform_0.11.10_linux_amd64.zip \
        && unzip terraform.zip \
        && rm terraform.zip \
        && mv terraform /usr/local/bin/terraform \
    && curl -Lo tflint.zip https://github.com/wata727/tflint/releases/download/v0.7.2/tflint_linux_amd64.zip \
        && unzip tflint.zip \
        && rm tflint.zip \
        && install tflint /usr/local/bin/ \
    && curl -Lo heptio-authenticator-aws https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.3.0/heptio-authenticator-aws_0.3.0_linux_amd64 \
        && chmod a+x heptio-authenticator-aws \
        && mv heptio-authenticator-aws /usr/local/bin/ \
    && curl -Lo helm.tar.gz https://storage.googleapis.com/kubernetes-helm/helm-v2.11.0-linux-amd64.tar.gz \
        && tar -zxvf helm.tar.gz \
        && mv linux-amd64/helm /usr/local/bin/ \
        && rm -rf helm.tar.gz linux-amd64 \
    && curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py \
        && python3 get-pip.py \
        && python get-pip.py \
        && rm get-pip.py \
    && pip3 install \
        selenium==3.141.0 \
        requests==2.20.1 \
    && pip install \
        awscli==1.16.55 \
        requests==2.20.1 \
    && curl -LSo geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz \
         && tar -zxvf geckodriver.tar.gz \
         && mv geckodriver /usr/local/bin/ \
         && rm geckodriver.tar.gz \
    && curl -LSo firefox.tar.bz2 https://download-installer.cdn.mozilla.net/pub/firefox/releases/63.0.3/linux-x86_64/en-US/firefox-63.0.3.tar.bz2 \
         && tar xjvf firefox.tar.bz2 \
         && mv firefox/ /opt \
         && ln -s /opt/firefox/firefox /usr/local/bin/firefox \
         && rm firefox.tar.bz2 \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - \
        && add-apt-repository \
            "deb [arch=amd64] https://download.docker.com/linux/debian \
            $(lsb_release -cs) stable" \
    && curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
        && touch /etc/apt/sources.list.d/kubernetes.list \
        && echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | tee -a /etc/apt/sources.list.d/kubernetes.list \
    && apt-get update && apt-get install --no-install-recommends -y \
        docker-ce \
        kubectl \
    && curl -LsSo vault.zip https://releases.hashicorp.com/vault/0.11.5/vault_0.11.5_linux_amd64.zip \
        && unzip vault.zip \
        && mv vault /usr/local/bin \
        && rm vault.zip \
    && curl -LsSo vaultenv.deb https://github.com/channable/vaultenv/releases/download/v0.9.0/vaultenv-0-9-0.deb \
        && dpkg -i vaultenv.deb \
        && rm vaultenv.deb \
    && rm -rf /var/lib/apt

CMD ["bash"]
