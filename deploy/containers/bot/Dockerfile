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
    && mkdir /usr/src/app/app/documentator/images  \
    && mkdir /usr/src/app/app/documentator/tpls  \
    && mkdir /usr/src/app/app/documentator/results  \
    && chown -R www-data:www-data  /usr/src/app/app/documentator \
    && chmod -R 0744 /usr/src/app/app/documentator \
    && torus run -- python /usr/src/app/deploy/containers/common/vars/render.py \
    && chown -R www-data:www-data /usr/src/app/ \
    && a2dismod python \
    && a2enmod ssl \
    && cd /usr/src/app/app/assets && npm install && cd \
    && torus run -- /root/vars/certs.sh \
    && echo "ServerTokens Prod" >> /etc/apache2/apache2.conf \
    && echo "ServerSignature Off" >> /etc/apache2/apache2.conf \
    && export TORUS_TOKEN_ID='' \
    && export TORUS_TOKEN_SECRET=''

# First command
CMD a2ensite integrates-ssl.conf \
&& a2ensite 000-default.conf \
&& torus run -- /usr/src/app/manage.py makemigrations \
&& torus run -- /usr/src/app/manage.py migrate \
&& torus run -- /usr/src/app/manage.py bot
