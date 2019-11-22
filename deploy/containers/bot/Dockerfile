ARG CI_COMMIT_REF_NAME
ARG ENV_NAME

FROM registry.gitlab.com/fluidattacks/integrates/deps-$ENV_NAME:$CI_COMMIT_REF_NAME

ARG CI_API_V4_URL
ARG CI_COMMIT_REF_NAME
ARG CI_PROJECT_ID
ARG ENV_NAME

ENV CI_COMMIT_REF_NAME $CI_COMMIT_REF_NAME
ENV VAULTENV_SECRETS_FILE /usr/src/app/env.vars

LABEL mantainer="engineering@fluidattacks.com"

WORKDIR /usr/src/app

# Put integrates in container
COPY . .

# Set prod or dev envars
RUN sed -i "s/env#/${ENV_NAME}#/g" env.vars

# Clean unnecessary apps
RUN apt-get remove --purge -y \
    apache2 \
    libapache2-mod-wsgi-py3 \
    nodejs \
    td-agent \
  && apt-get -y autoremove

# Start integrates bot
CMD vaultenv ./deploy/containers/common/vars/run.sh bot
