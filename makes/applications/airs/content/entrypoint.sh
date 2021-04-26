# shellcheck shell=bash

function main {
  local url='https://please-replace-this-url-before-deploying'
  local out="${1}"

      pushd "${out}" \
    &&  mkdir new-front \
    &&  aws_login_dev airs \
    &&  sops_export_vars __envAirsSecrets__/development.yaml \
          CLOUDINARY_API_SECRET \
          CLOUDINARY_API_KEY \
          CLOUDINARY_CLOUD_NAME \
    &&  copy __envAirsNewFront__ new-front \
    &&  copy __envAirsContent__ new-front/content \
    &&  copy __envAirsContentPages__ new-front/static/images \
    &&  find new-front/static/images -type f ! -regex ".*\.\(svg\|gif\|png\|mp4\)" -delete \
    &&  copy __envAirsContentImages__ new-front/static/images \
    &&  copy __envAirsImages__ new-front/static/images \
    &&  sed -i "s|https://fluidattacks.com/new-front|${url}|g" new-front/gatsby-config.js \
    &&  if test -n "${CI:-}" && test "${CI_COMMIT_REF_NAME}" != "master"
        then
          sed -i "s|pathPrefix: '/new-front'|pathPrefix: '${CI_COMMIT_REF_NAME}/new-front'|g" new-front/gatsby-config.js
        fi \
    &&  pushd new-front \
      &&  find content/pages -type f -name "*.adoc" -exec sed -i 's|:slug|:page-slug|g' {} + \
      &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:description|:page-description|g" {} + \
      &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:keywords|:page-keywords|g" {} + \
      &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:template: solution|:page-template: solution|g" {} + \
      &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:template: solutions|:page-template: solutions|g" {} + \
      &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:template: services/continuous|:page-template: service|g" {} + \
      &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:template: services/one-shot|:page-template: service|g" {} + \
      &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:definition:|:page-definition:|g" {} + \
      &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:banner|:page-banner|g" {} + \
      &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:subtitle|:page-subtitle|g" {} + \
      &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:subtext|:page-subtext|g" {} + \
      &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:solution|:page-solution|g" {} + \
      &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|../theme/images|../images|g" {} + \
      &&  rm -rf \
            content/pages/about-us/clients \
            content/pages/products/defends \
            content/pages/products/rules \
      &&  copy __envAirsNpm__/node_modules 'node_modules' \
      &&  HOME=. ./node_modules/.bin/gatsby build --prefix-paths \
    &&  popd \
      &&  mv new-front/public . \
      &&  rm -rf new-front/* \
      &&  copy public new-front \
      &&  rm -rf public \
  &&  popd \
  ||  return 1
}

main "${@}"

