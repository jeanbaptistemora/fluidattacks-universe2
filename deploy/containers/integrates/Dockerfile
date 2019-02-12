FROM fluid-docker.jfrog.io/integrates:deps190201

# Doubts about the image in question
MAINTAINER FLUID Engineering Team <engineering@fluidattacks.com>

ARG ci_commit_ref_name
ARG gitlab_login
ARG gitlab_password
ARG drive_authorization
ARG drive_authorization_client
ARG documentroot
ARG ssl_key
ARG ssl_cert
ARG vault_env
ARG fi_version

ENV CI_COMMIT_REF_NAME=$ci_commit_ref_name
ENV FI_VERSION=$fi_version
ENV VAULTENV_SECRETS_FILE=/usr/src/app/env.vars

# Add variables
ADD common/vars* /root/vars

# Change root directory
WORKDIR /root/

# Remove index file, clone Integrates repository CI_COMMIT_REF_NAME and execute ansible
RUN rm -r /var/www/html \
    && git clone --depth 1 -b $CI_COMMIT_REF_NAME \
         https://"$gitlab_login":"$gitlab_password"@gitlab.com/fluidattacks/integrates.git  \
         /usr/src/app \
    && curl -L https://toolbelt.treasuredata.com/sh/install-debian-stretch-td-agent2.sh | sh \
    && rm -f /etc/td-agent/td-agent.conf \
    && mv /usr/src/app/deploy/containers/common/vars/fluent.conf /etc/td-agent/td-agent.conf \
    && rm -f /etc/init.d/td-agent \
    && mv /usr/src/app/deploy/containers/common/vars/td-agent /etc/init.d/td-agent && chmod 0755 /etc/init.d/td-agent  \
    && mv /usr/src/app/deploy/containers/common/vars/out_rollbar.rb /etc/td-agent/plugin/ \
    && /usr/sbin/td-agent-gem install eventmachine em-http-request fluent-plugin-rewrite-tag-filter \
    && mkdir /usr/src/app/app/documentator/images  \
    && mkdir /usr/src/app/app/documentator/tpls  \
    && mkdir /usr/src/app/app/documentator/results  \
    && mkdir /usr/src/app/app/techdoc/results  \
    && chown -R www-data:www-data  /usr/src/app/app/documentator \
    && chmod -R 0744 /usr/src/app/app/documentator \
    && chown -R www-data:www-data  /usr/src/app/app/techdoc \
    && chmod -R 0744 /usr/src/app/app/techdoc \
    && export FI_DRIVE_AUTHORIZATION=$(echo "$drive_authorization" | base64 -d) \
    && export FI_DRIVE_AUTHORIZATION_CLIENT=$(echo "$drive_authorization_client" | base64 -d) \
    && export FI_DOCUMENTROOT="$documentroot" \
    && python /usr/src/app/deploy/containers/common/vars/render.py \
    && chown -R www-data:www-data /usr/src/app/ \
    && a2dismod python \
    && a2dismod -f deflate \
    && a2enmod ssl \
    && cd /usr/src/app/app/assets && npm install && cd \
    && echo "$ssl_cert" | base64 -di > "/etc/ssl/certs/fluidla.crt" \
    && echo "$ssl_key" | base64 -di > "/etc/ssl/private/fluidla.key" \
    && echo "ServerTokens Prod" >> /etc/apache2/apache2.conf \
    && echo "ServerSignature Off" >> /etc/apache2/apache2.conf \
    && cd /usr/src/app/front/ && npm install && gulp \
    && sed -i 's/>v./>v.\ '"${FI_VERSION}"'/' /usr/src/app/app/templates/dashboard.html \
    && sed -i 's/env#/'"$vault_env"'#/g' /usr/src/app/env.vars

# Make port 443 and 24224 available to the world outside this container
EXPOSE 443 24224

# First command
CMD vaultenv vars/run.sh
