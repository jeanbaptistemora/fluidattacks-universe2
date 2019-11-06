FROM debian:buster

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf8

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
        procps \
        python \
        python3 \
        python-dev \
        python3-dev \
        software-properties-common \
        unzip \
        wget \
        apt-utils \
    && curl -o terraform.zip https://releases.hashicorp.com/terraform/0.12.13/terraform_0.12.13_linux_amd64.zip \
        && unzip terraform.zip \
        && rm terraform.zip \
        && mv terraform /usr/local/bin/terraform \
    && curl -Lo tflint.zip https://github.com/wata727/tflint/releases/download/v0.12.1/tflint_linux_amd64.zip \
        && unzip tflint.zip \
        && rm tflint.zip \
        && mv tflint /usr/local/bin/ \
    && curl -Lo heptio-authenticator-aws https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.3.0/heptio-authenticator-aws_0.3.0_linux_amd64 \
        && chmod a+x heptio-authenticator-aws \
        && mv heptio-authenticator-aws /usr/local/bin/ \
    && curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.14.6/2019-08-22/bin/linux/amd64/aws-iam-authenticator \
        && chmod +x aws-iam-authenticator \
        && mv aws-iam-authenticator /usr/local/bin/ \
    && curl -Lo helm.tar.gz https://storage.googleapis.com/kubernetes-helm/helm-v2.11.0-linux-amd64.tar.gz \
        && tar -zxvf helm.tar.gz \
        && mv linux-amd64/helm /usr/local/bin/ \
        && rm -rf helm.tar.gz linux-amd64 \
    && curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py \
        && python3 get-pip.py \
        && python get-pip.py \
        && rm get-pip.py \
    && pip3 install \
        GitPython==2.1.11 \
        mandrill-37==1.1.0 \
        pre-commit==1.14.2 \
        prospector[with_everything]==1.1.6.2 \
        requests==2.20.1 \
        selenium==3.141.0 \
        urllib3==1.25.3 \
        yq==2.9.2 \
    && pip install \
        awscli==1.16.55 \
        requests==2.20.1 \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
        && sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
        && apt-get -y update \
        && apt-get -y install google-chrome-stable \
    && wget -N http://chromedriver.storage.googleapis.com/2.44/chromedriver_linux64.zip -P ~/ \
        && unzip ~/chromedriver_linux64.zip -d ~/ \
        && rm ~/chromedriver_linux64.zip \
        && mv -f ~/chromedriver /usr/local/bin/chromedriver \
        && chown root:root /usr/local/bin/chromedriver \
        && chmod 0755 /usr/local/bin/chromedriver \
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
    && curl -LsSo sops.deb https://github.com/mozilla/sops/releases/download/3.4.0/sops_3.4.0_amd64.deb \
        && dpkg -i sops.deb \
        && rm sops.deb \
    && rm -rf /var/lib/apt

CMD ["bash"]
