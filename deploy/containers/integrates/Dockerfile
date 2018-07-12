# Last stable Debian base image (jessie-slim)
FROM registry.gitlab.com/fluidsignal/integrates:deps

# Doubts about the image in question
MAINTAINER FLUID Engineering Team <engineering@fluidattacks.com>

ARG ci_commit_ref_name
ARG torus_token_id
ARG torus_token_secret
ARG torus_org
ARG torus_project
ARG torus_environment

ENV CI_COMMIT_REF_NAME=$ci_commit_ref_name
ENV TORUS_ORG=$torus_org
ENV TORUS_PROJECT=$torus_project
ENV TORUS_ENVIRONMENT=$torus_environment

# Add variables
ADD common/vars* /root/vars

# Change root directory
WORKDIR /root/

# Remove index file, clone Integrates repository CI_COMMIT_REF_NAME and execute ansible
RUN rm -r /var/www/html \
    && export TORUS_TOKEN_ID=$torus_token_id \
    && export TORUS_TOKEN_SECRET=$torus_token_secret \
    && torus run -- /root/vars/clone.sh \
    && gem install asciidoctor-pdf --pre \
    && apt-get install -y ruby-dev \
    && curl -L https://toolbelt.treasuredata.com/sh/install-debian-jessie-td-agent2.sh | sh \
    && rm /etc/td-agent/td-agent.conf \
    && mv /usr/src/app/deploy/containers/common/vars/fluent.conf /etc/td-agent/td-agent.conf \
    && rm /etc/init.d/td-agent \
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
    && torus run -- python /usr/src/app/deploy/containers/common/vars/render.py \
    && chown -R www-data:www-data /usr/src/app/ \
    && a2dismod python \
    && a2dismod -f deflate \
    && a2enmod ssl \
    && cd /usr/src/app/app/assets && npm install && cd \
    && torus run -- /root/vars/certs.sh \
    && echo "ServerTokens Prod" >> /etc/apache2/apache2.conf \
    && echo "ServerSignature Off" >> /etc/apache2/apache2.conf \
    && export TORUS_TOKEN_ID='' \
    && export TORUS_TOKEN_SECRET='' \
    && npm install -g typescript@2.9.2 browserify@16.2.2 uglify-js@3.4.3 tslint@5.10.0 \
    && cd /usr/src/app/app/assets/login \
    && tsc -p tsconfig.json \ 
    && browserify index.js | uglifyjs  > bundle.min.js \
    && cd /usr/src/app && python -c 'import integrates_version; integrates_version.set_integrates_version()' \
    && cd /usr/src/app/front \
    && mkdir -p /usr/src/app/app/assets/dashboard/ \
    && npm install \
    && tsc -p tsconfig.json \ 
    && browserify build/index.js | uglifyjs  > /usr/src/app/app/assets/dashboard/bundle.min.js

# Make port 443 and 24224 available to the world outside this container
EXPOSE 443 24224

# First command
CMD env > /etc/environment \
&& /etc/init.d/td-agent restart \
&& a2ensite integrates-ssl.conf \
&& a2ensite 000-default.conf \
&& torus run -- /usr/src/app/manage.py makemigrations \
&& torus run -- /usr/src/app/manage.py migrate \
&& torus run -- /usr/src/app/manage.py crontab add \
&& if [ "$CI_COMMIT_REF_NAME" = "master" ]; then /root/vars/cron.sh; fi \
&& torus run -- /usr/sbin/apache2ctl -D FOREGROUND
