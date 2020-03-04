ARG CI_COMMIT_REF_NAME

FROM "registry.gitlab.com/fluidattacks/web/builder:${CI_COMMIT_REF_NAME}" as compiler

ARG CI_COMMIT_REF_NAME

RUN pybabel compile --directory theme/2014/translations/ --domain messages \
    && sed -i "s|https://fluidattacks.com|https://web.env.fluidattacks.com/${CI_COMMIT_REF_NAME}|g" pelicanconf.py \
    && cp -a deploy/builder/node_modules theme/2014/ \
    && cp -a deploy/builder/node_modules /app/ \
    && npm run --prefix deploy/builder/ build \
    && ./build-site.sh \
    && ./html-lint.sh

FROM nginx:stable-alpine
COPY --from=compiler /app/output/web /usr/share/nginx/html/web

CMD ["nginx", "-g", "daemon off;"]
