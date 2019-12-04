FROM debian:buster-slim

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf8

ARG URL_TERRAFORM='https://releases.hashicorp.com/terraform/0.12.17/terraform_0.12.17_linux_amd64.zip'
ARG URL_TFLINT='https://github.com/terraform-linters/tflint/releases/download/v0.13.1/tflint_linux_amd64.zip'
ARG URL_HEPTIO_AUTH='https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.3.0/heptio-authenticator-aws_0.3.0_linux_amd64'
ARG URL_AWS_IAM_AUTH='https://amazon-eks.s3-us-west-2.amazonaws.com/1.14.6/2019-08-22/bin/linux/amd64/aws-iam-authenticator'
ARG URL_HELM='https://storage.googleapis.com/kubernetes-helm/helm-v2.11.0-linux-amd64.tar.gz'
ARG URL_KUBECTL='https://storage.googleapis.com/kubernetes-release/release/v1.16.2/bin/linux/amd64/kubectl'
ARG URL_VAULT='https://releases.hashicorp.com/vault/0.11.5/vault_0.11.5_linux_amd64.zip'
ARG URL_SOPS='https://github.com/mozilla/sops/releases/download/3.4.0/sops_3.4.0_amd64.deb'

# Apt deps
RUN apt update \
  && apt upgrade -y \
  && apt-get install --no-install-recommends -y \
    curl \
    gettext-base \
    git \
    jq \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    unzip \
    wget

# External deps
RUN wget -O terraform.zip "$URL_TERRAFORM" \
    && unzip terraform.zip \
    && rm terraform.zip \
    && mv terraform /usr/local/bin/terraform \
  && wget -O tflint.zip "$URL_TFLINT" \
    && unzip tflint.zip \
    && rm tflint.zip \
    && mv tflint /usr/local/bin/ \
  && wget -O heptio-authenticator-aws "$URL_HEPTIO_AUTH" \
    && chmod a+x heptio-authenticator-aws \
    && mv heptio-authenticator-aws /usr/local/bin/ \
  && wget -O aws-iam-authenticator "$URL_AWS_IAM_AUTH" \
    && chmod +x aws-iam-authenticator \
    && mv aws-iam-authenticator /usr/local/bin/ \
  && wget -O helm.tar.gz "$URL_HELM" \
    && tar -zxvf helm.tar.gz \
    && mv linux-amd64/helm /usr/local/bin/ \
    && rm -rf helm.tar.gz linux-amd64 \
  && wget -O kubectl "$URL_KUBECTL" \
    && chmod +x kubectl \
    && mv kubectl /usr/local/bin/kubectl \
  && wget -O vault.zip "$URL_VAULT" \
    && unzip vault.zip \
    && mv vault /usr/local/bin \
    && rm vault.zip \
  && wget -O sops.deb "$URL_SOPS" \
    && dpkg -i sops.deb \
    && rm sops.deb

# Pip deps
RUN pip3 install \
    GitPython==2.1.11 \
    mandrill-37==1.1.0 \
    pre-commit==1.14.2 \
    prospector[with_everything]==1.1.6.2 \
    requests==2.20.1 \
    urllib3==1.25.3 \
    yq==2.9.2 \
    awscli==1.16.55

CMD ["bash"]
