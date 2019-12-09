ARG CI_COMMIT_REF_NAME

FROM registry.gitlab.com/fluidattacks/integrates/deps-base:$CI_COMMIT_REF_NAME

ARG PATCHES='deploy/containers/deps-production'
ARG PIP_REQUIREMENTS='deploy/containers/deps-production/requirements.txt'
ARG PIP_REQUIREMENTS_PROD_LOCAL='deploy/containers/deps-production/requirements_local.txt'

COPY "$PIP_REQUIREMENTS" /tmp
COPY "$PATCHES/enable_redis_cluster_sessions.diff" /tmp
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt \
  && cat /tmp/enable_redis_cluster_sessions.diff \
    | patch -d /usr/local/lib/python3.7/dist-packages/redis_sessions -p1

# npm deps. node_modules folders are stored in /npm-deps
# make sure to copy them to the required folder if needed.
COPY front /tmp/front
RUN npm install -g secure-spreadsheet@0.1.0 \
  && mkdir -p /npm-deps/front \
  && npm install --prefix /tmp/front --only=production \
  && npm cache clean --force \
  && mv /tmp/front/node_modules /npm-deps/front/

# local apps
COPY "$PIP_REQUIREMENTS_PROD_LOCAL" /tmp/reqs_prod_local.txt
COPY django-apps/packages/* django-apps/packages/
RUN pip3 install --no-cache-dir --no-index \
    --find-links=django-apps/packages/ -r /tmp/reqs_prod_local.txt
