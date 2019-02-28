FROM fluid-docker.jfrog.io/integrates:deps

ARG CI_COMMIT_REF_NAME
ARG CI_REPOSITORY_URL
ARG DOCUMENTROOT
ARG DRIVE_AUTHORIZATION
ARG DRIVE_AUTHORIZATION_CLIENT
ARG ENV_NAME
ARG SSL_CERT
ARG SSL_KEY

ENV CI_COMMIT_REF_NAME ${CI_COMMIT_REF_NAME}
ENV VAULTENV_SECRETS_FILE /usr/src/app/env.vars

LABEL mantainer="engineering@fluidattacks.com"

ADD vars /root/vars

WORKDIR /root/

RUN git clone --depth 1 -b "${CI_COMMIT_REF_NAME}" "${CI_REPOSITORY_URL}" /usr/src/app \
    && rm -r /var/www/html \
    && mkdir /usr/src/app/app/documentator/images  \
    && mkdir /usr/src/app/app/documentator/tpls  \
    && mkdir /usr/src/app/app/documentator/results  \
    && chown -R www-data:www-data  /usr/src/app/app/documentator \
    && chmod -R 0744 /usr/src/app/app/documentator \
    && export FI_DRIVE_AUTHORIZATION=$(echo "${DRIVE_AUTHORIZATION}" | base64 -d) \
    && export FI_DRIVE_AUTHORIZATION_CLIENT=$(echo "${DRIVE_AUTHORIZATION_CLIENT}" | base64 -d) \
    && export FI_DOCUMENTROOT="${DOCUMENTROOT}" \
    && python /usr/src/app/deploy/containers/common/vars/render.py \
    && chown -R www-data:www-data /usr/src/app/ \
    && a2dismod python \
    && a2enmod ssl \
    && cd /usr/src/app/app/assets && npm install && cd \
    && echo "${SSL_CERT}" | base64 -di > "/etc/ssl/certs/fluidla.crt" \
    && echo "${SSL_KEY}" | base64 -di > "/etc/ssl/private/fluidla.key" \
    && echo "ServerTokens Prod" >> /etc/apache2/apache2.conf \
    && echo "ServerSignature Off" >> /etc/apache2/apache2.conf \
    && sed -i 's/env#/'"${ENV_NAME}"'#/g' /usr/src/app/env.vars

CMD vaultenv vars/run.sh
