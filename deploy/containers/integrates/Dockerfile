FROM registry.gitlab.com/fluidsignal/default/integrates/deps:app

ARG CI_API_V4_URL
ARG CI_COMMIT_REF_NAME
ARG CI_PROJECT_ID
ARG DOCUMENTROOT
ARG DRIVE_AUTHORIZATION
ARG DRIVE_AUTHORIZATION_CLIENT
ARG ENV_NAME
ARG SSL_CERT
ARG SSL_KEY
ARG VERSION

ENV CI_COMMIT_REF_NAME ${CI_COMMIT_REF_NAME}
ENV FI_VERSION ${VERSION}
ENV VAULTENV_SECRETS_FILE /usr/src/app/env.vars

LABEL mantainer="engineering@fluidattacks.com"

RUN curl -Lo integrates.tar.gz "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/repository/archive.tar.gz?sha=${CI_COMMIT_REF_NAME}" \
        && tar zxf integrates.tar.gz \
        && rm integrates.tar.gz \
        && mv integrates-* /usr/src/app \
    && rm -r /var/www/html \
    && rm -f /etc/td-agent/td-agent.conf \
        && mv /usr/src/app/deploy/containers/common/vars/fluent.conf /etc/td-agent/td-agent.conf \
        && rm -f /etc/init.d/td-agent \
        && mv /usr/src/app/deploy/containers/common/vars/td-agent /etc/init.d/td-agent && chmod 0755 /etc/init.d/td-agent  \
        && mv /usr/src/app/deploy/containers/common/vars/out_rollbar.rb /etc/td-agent/plugin/ \
    && mkdir /usr/src/app/app/documentator/images  \
        && mkdir /usr/src/app/app/documentator/tpls  \
        && mkdir /usr/src/app/app/documentator/results  \
        && mkdir /usr/src/app/app/techdoc/results  \
        && chown -R www-data:www-data  /usr/src/app/app/documentator \
        && chmod -R 0744 /usr/src/app/app/documentator \
        && chown -R www-data:www-data  /usr/src/app/app/techdoc \
        && chmod -R 0744 /usr/src/app/app/techdoc \
    && export FI_DRIVE_AUTHORIZATION=$(echo "${DRIVE_AUTHORIZATION}" | base64 -d) \
        && export FI_DRIVE_AUTHORIZATION_CLIENT=$(echo "${DRIVE_AUTHORIZATION_CLIENT}" | base64 -d) \
        && export FI_DOCUMENTROOT="${DOCUMENTROOT}" \
        && python /usr/src/app/deploy/containers/common/vars/render.py \
    && chown -R www-data:www-data /usr/src/app/ \
        && a2dismod -f deflate \
        && a2enmod ssl \
    && cp -a /root/assets/node_modules /usr/src/app/app/assets/ \
        && cd /usr/src/app/app/assets \
        && npm install \
        && npm cache clean --force \
    && cp -a /root/front/node_modules /usr/src/app/front \
        && cd /usr/src/app/front/ \
        && npm install \
        && npm cache clean --force \
    && cp -a /usr/src/app/deploy/containers/common/vars/run.sh /root \
    && echo "${SSL_CERT}" | base64 -di > "/etc/ssl/certs/fluidla.crt" \
        && echo "${SSL_KEY}" | base64 -di > "/etc/ssl/private/fluidla.key" \
        && echo "ServerTokens Prod" >> /etc/apache2/apache2.conf \
        && echo "ServerSignature Off" >> /etc/apache2/apache2.conf \
    && sed -i 's/>v./>v.\ '"${FI_VERSION}"'/' /usr/src/app/app/templates/dashboard.html \
    && sed -i 's/env#/'"${ENV_NAME}"'#/g' /usr/src/app/env.vars \
    && apt-get remove --purge -y \
         cron \
         nodejs \
    && apt-get -y autoremove \
    && rm -rf \
        /root/front \
        /root/assets

COPY dashboard /usr/src/app/app/assets/dashboard

EXPOSE 443 24224

CMD vaultenv ./run.sh
