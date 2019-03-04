FROM fluid-docker.jfrog.io/integrates:deps

ARG CI_API_V4_URL
ARG CI_COMMIT_REF_NAME
ARG CI_PROJECT_ID
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

RUN curl -Lo integrates.tar.gz "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/repository/archive.tar.gz?sha=${CI_COMMIT_REF_NAME}" \
        && tar zxf integrates.tar.gz \
        && rm integrates.tar.gz \
        && mv integrates-* /usr/src/app \
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
    && a2enmod ssl \
    && cp -a /root/assets/node_modules /usr/src/app/app/assets/ \
        && cd /usr/src/app/app/assets && npm install \
    && rm -rf /root/front /root/assets \
    && echo "${SSL_CERT}" | base64 -di > "/etc/ssl/certs/fluidla.crt" \
        && echo "${SSL_KEY}" | base64 -di > "/etc/ssl/private/fluidla.key" \
        && echo "ServerTokens Prod" >> /etc/apache2/apache2.conf \
        && echo "ServerSignature Off" >> /etc/apache2/apache2.conf \
    && sed -i 's/env#/'"${ENV_NAME}"'#/g' /usr/src/app/env.vars

CMD vaultenv vars/run.sh
