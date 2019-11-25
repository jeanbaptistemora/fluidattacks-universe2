ARG CI_COMMIT_REF_NAME

FROM registry.gitlab.com/fluidattacks/integrates/deps-base:$CI_COMMIT_REF_NAME

ARG PATCHES='deploy/containers/deps-production'
ARG PIP_REQUIREMENTS='deploy/containers/deps-production/requirements.txt'

# python deps
COPY "$PIP_REQUIREMENTS" /tmp
RUN pip3 install -U setuptools==41.4.0 && \
    pip3 install --no-cache-dir -r /tmp/requirements.txt

# ruby deps
RUN gem install -N asciidoctor:1.5.8 concurrent-ruby \
  && gem install -N asciidoctor-pdf:1.5.0.alpha.16 --pre \
  && /usr/sbin/td-agent-gem install \
    eventmachine \
    em-http-request \
    fluent-plugin-rewrite-tag-filter

# npm deps. node_modules folders are stored in /npm-deps
# make sure to copy them to the required folder if needed.
COPY front /tmp/front
RUN npm install -g secure-spreadsheet@0.1.0 \
  && mkdir -p /npm-deps/front \
  && npm install --prefix /tmp/front --only=production \
  && npm cache clean --force \
  && mv /tmp/front/node_modules /npm-deps/front/

# patches and cleans
COPY "$PATCHES/enable_redis_cluster_sessions.diff" /tmp
RUN cat /tmp/enable_redis_cluster_sessions.diff \
    | patch -d /usr/local/lib/python3.7/dist-packages/redis_sessions -p1
