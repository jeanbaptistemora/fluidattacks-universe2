FROM registry.gitlab.com/fluidsignal/default/integrates/deps:app

ARG CI_API_V4_URL
ARG CI_COMMIT_REF_NAME
ARG CI_PROJECT_ID
ARG ENV_NAME

ENV CI_COMMIT_REF_NAME ${CI_COMMIT_REF_NAME}
ENV VAULTENV_SECRETS_FILE /usr/src/app/env.vars

LABEL mantainer="engineering@fluidattacks.com"

RUN curl -Lo integrates.tar.gz "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/repository/archive.tar.gz?sha=${CI_COMMIT_REF_NAME}" \
        && tar zxf integrates.tar.gz \
        && rm integrates.tar.gz \
        && mv integrates-* /usr/src/app \
    && cp -a /usr/src/app/deploy/containers/common/vars/run.sh /root \
    && cp -a /usr/src/app/deploy/containers/common/vars/cron.sh /root \
    && sed -i 's/env#/'"${ENV_NAME}"'#/g' /usr/src/app/env.vars \
    && apt-get remove --purge -y \
        apache2 \
        libapache2-mod-wsgi \
        nodejs \
        td-agent \
    && apt-get -y autoremove \
    && rm -rf \
        /root/front \
        /root/assets

CMD vaultenv ./run.sh
