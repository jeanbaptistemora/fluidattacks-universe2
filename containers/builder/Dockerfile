FROM debian:jessie-slim

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
        apt-transport-https \
        ca-certificates \
        curl \
        git \
        gnupg2 \
        jq \
        lsb-release \
        openssh-client \
        python \
        python-dev \
        python-pip \
        software-properties-common \
        unzip \
    && curl -o terraform.zip https://releases.hashicorp.com/terraform/0.11.7/terraform_0.11.7_linux_amd64.zip \
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
    && pip install --upgrade pip \
        && pip install awscli \
    && DISTRO=$(lsb_release -i | awk '{print tolower($3)}') \
        && CODENAME=$(lsb_release -c | awk '{print $2}') \
        && echo "deb https://get.torus.sh/$DISTRO/ $CODENAME main" | tee -a /etc/apt/sources.list.d/torus.list \
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
        torus \
    && curl -Lo go.tar.gz https://dl.google.com/go/go1.10.2.linux-amd64.tar.gz \
        && tar -C /usr/local -xzf go.tar.gz \
        && rm go.tar.gz \
    && rm -rf /var/lib/apt

ENV PATH=$PATH:/usr/local/go/bin/

CMD ["bash"]
