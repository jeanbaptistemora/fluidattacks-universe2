ARG CI_COMMIT_REF_NAME

FROM registry.gitlab.com/fluidattacks/integrates/deps-base:$CI_COMMIT_REF_NAME

ARG VAULT_URL='https://releases.hashicorp.com/vault/0.11.6/vault_0.11.6_linux_amd64.zip'
ARG GECKO_DRIVER_URL='https://chromedriver.storage.googleapis.com/78.0.3904.105/chromedriver_linux64.zip'
ARG GOOGLE_CHROME_URL='https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'
ARG CHROME_SIGNING_KEY='https://dl.google.com/linux/linux_signing_key.pub'
ARG DYNAMODB_LOCAL_URL='https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz'
ARG PIP_REQUIREMENTS_DEV='deploy/containers/deps-development/requirements.txt'
ARG PIP_REQUIREMENTS_PROD='deploy/containers/deps-production/requirements.txt'
ARG TERRAFORM_URL='https://releases.hashicorp.com/terraform/0.12.16/terraform_0.12.16_linux_amd64.zip'
ARG KUBECTL_URL='https://storage.googleapis.com/kubernetes-release/release/v1.16.2/bin/linux/amd64/kubectl'

RUN mkdir -p /usr/share/man/man1 \
  && apt -o Acquire::Check-Valid-Until=false update \
  && apt install -yo DPkg::Options::='--force-confnew' --no-install-recommends \
    unzip \
    jq \
    wget \
    gettext-base \
    default-jre \
    xdg-utils \
    lsb-release \
    libxss1 \
    libappindicator3-1 \
    fonts-liberation \
  && wget -q -O - "$CHROME_SIGNING_KEY" | sudo apt-key add - \
  && curl -Lo google-chrome.deb "$GOOGLE_CHROME_URL" \
    && dpkg -i google-chrome.deb \
    && rm google-chrome.deb \
  && curl -LsSo vault.zip "$VAULT_URL" \
    && unzip vault.zip \
    && mv vault /usr/local/bin \
    && rm vault.zip \
  && curl -Lo chromedriver.zip "$GECKO_DRIVER_URL" \
    && unzip chromedriver.zip \
    && mv chromedriver /usr/bin \
    && rm chromedriver.zip \
  && curl -Lo dynamodb_local.tar.gz "$DYNAMODB_LOCAL_URL" \
    && mkdir -p /usr/local/lib/dynamodb-local \
    && tar xzf dynamodb_local.tar.gz -C /usr/local/lib/dynamodb-local \
    && rm dynamodb_local.tar.gz \
  && curl -o terraform.zip "$TERRAFORM_URL" \
    && unzip terraform.zip \
    && rm terraform.zip \
    && mv terraform /usr/local/bin/terraform \
  && curl -o kubectl "$KUBECTL_URL" \
    && chmod +x kubectl \
    && mv kubectl /usr/local/bin/kubectl \
  && a2enmod proxy \
  && a2enmod proxy_http \
  && a2enmod rewrite \
  && a2enmod substitute

COPY "$PIP_REQUIREMENTS_DEV" /tmp/reqs_dev.txt
COPY "$PIP_REQUIREMENTS_PROD" /tmp/reqs_prod.txt
RUN pip3 install --no-cache-dir -r /tmp/reqs_prod.txt \
  && pip3 install --no-cache-dir -r /tmp/reqs_dev.txt

# npm deps. node_modules folders are stored in /npm-deps,
# make sure to copy them to the required folder if needed.
# In this stage, production node_modules built in deps-production
# container are taken to /tmp/front. Then, development deps install
# on top of it and finally, the new node_modules is moved to
# /npm-deps again

ADD front/package.json /tmp/front/package.json
RUN npm install -g secure-spreadsheet@0.1.0 \
  && mkdir -p /npm-deps/front \
  && npm install --prefix /tmp/front --only=production \
  && npm install --prefix /tmp/front --only=development \
  && npm cache clean --force \
  && mv /tmp/front/node_modules /npm-deps/front/
