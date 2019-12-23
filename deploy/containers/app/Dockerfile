ARG CI_COMMIT_REF_NAME
ARG ENV_NAME

FROM registry.gitlab.com/fluidattacks/integrates/deps-$ENV_NAME:$CI_COMMIT_REF_NAME

ARG CI_API_V4_URL
ARG CI_COMMIT_REF_NAME
ARG CI_PROJECT_ID
ARG ENV_NAME
ARG SSL_CERT
ARG SSL_KEY
ARG VERSION
ARG PIP_REQUIREMENTS_PROD_LOCAL='deploy/containers/deps-production/requirements_local.txt'

ENV CI_COMMIT_REF_NAME $CI_COMMIT_REF_NAME
ENV FI_VERSION $VERSION
ENV VAULTENV_SECRETS_FILE /usr/src/app/env.vars

LABEL mantainer="engineering@fluidattacks.com"

WORKDIR /usr/src/app

# Put integrates in container
COPY . .

# Replace td-agent configurations
RUN rm -rf /var/www/html \
  && rm -f /etc/td-agent/td-agent.conf \
  && rm -f /etc/init.d/td-agent \
  && mv deploy/containers/common/vars/fluent.conf /etc/td-agent/td-agent.conf \
  && mv deploy/containers/common/vars/td-agent /etc/init.d/td-agent \
    && chmod 0755 /etc/init.d/td-agent \
  && mv deploy/containers/common/vars/out_rollbar.rb /etc/td-agent/plugin/ \
  && mkdir app/documentator/images \
  && mkdir app/documentator/tpls \
  && mkdir app/documentator/results \
  && mkdir app/techdoc/results \
  && echo "$SSL_CERT" | base64 -di > /etc/ssl/certs/fluidla.crt \
  && echo "$SSL_KEY" | base64 -di > /etc/ssl/private/fluidla.key

# Compile front
RUN cp -a /npm-deps/front/node_modules front/ \
  && npm run --prefix front/ build \
  && sed -i "s/integrates_version/v. $FI_VERSION/g" app/assets/dashboard/app-bundle.min.js \
  && rm -rf front/node_modules

# local apps
COPY "$PIP_REQUIREMENTS_PROD_LOCAL" /tmp/reqs_prod_local.txt
COPY django-apps/packages/* django-apps/packages/
RUN sed -i "s/env#/${ENV_NAME}#/g" env.vars \
  && pip3 install --no-cache-dir --no-index \
    --find-links=django-apps/packages/ -r /tmp/reqs_prod_local.txt \
  && apt -y autoremove \
  && rm -rf /tmp/*

EXPOSE 80 24224

# Start integrates
CMD ./deploy/containers/common/vars/run.sh
