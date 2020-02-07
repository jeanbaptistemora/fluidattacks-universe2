ARG CI_COMMIT_REF_NAME
ARG REGISTRY_IMAGE
FROM ${REGISTRY_IMAGE}:${CI_COMMIT_REF_NAME} as cache


FROM registry.gitlab.com/fluidattacks/web:base

ARG CI_COMMIT_REF_NAME
ARG CI_PROJECT_NAME
ARG CI_PROJECT_NAMESPACE
ARG CI_REPOSITORY_URL
ARG ENV_DNS
ARG REGISTRY_IMAGE

RUN git clone --depth=1 -b "${CI_COMMIT_REF_NAME}" "${CI_REPOSITORY_URL}" /home/web

WORKDIR /home/web/

COPY --from=cache /home/cache /home/web/cache

RUN pybabel compile --directory theme/2014/translations/ --domain messages \
    && for FILE in $(find . -iname '*.adoc'); do \
      sed -i 's#^include::#include::/home#g' $FILE; \
      done \
    && sed -i 's/https:\/\/fluidattacks\.com/https:\/\/'"${CI_PROJECT_NAME}.${ENV_DNS}\/${CI_COMMIT_REF_NAME}"'/g' pelicanconf.py \
    && npm --prefix builder/base/ install \
    && cp -a builder/base/node_modules theme/2014/ \
    && npm run --prefix builder/base/ build \
    && ./build-site.sh \
    && ./html-lint.sh


FROM nginx:stable-alpine
COPY --from=1 /home/web/cache /home/cache
COPY --from=1 /home/web/output/web /usr/share/nginx/html/web
CMD ["nginx", "-g", "daemon off;"]
