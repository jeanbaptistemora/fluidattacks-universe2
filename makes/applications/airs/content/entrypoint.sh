# shellcheck shell=bash

function main {
  local url='https://please-replace-this-url-before-deploying'
  local out="airs/front"

        pushd "${out}" \
    &&  aws_login_dev airs \
    &&  sops_export_vars __envAirsSecrets__/development.yaml \
          CLOUDINARY_API_SECRET \
          CLOUDINARY_API_KEY \
          CLOUDINARY_CLOUD_NAME \
          FONTAWESOME_NPM_AUTH_TOKEN \
          GATSBY_ALGOLIA_APP_ID \
          GATSBY_ALGOLIA_SEARCH_KEY \
          ALGOLIA_ADMIN_KEY \
    &&  copy __envAirsContent__ content \
    &&  sed -i "s|https://fluidattacks.com|${url}|g" gatsby-config.js \
    &&  if test -n "${CI:-}" && test "${CI_COMMIT_REF_NAME}" != "master"
        then
          sed -i "s|pathPrefix: '/front'|pathPrefix: '/${CI_COMMIT_REF_NAME}'|g" gatsby-config.js
        fi \
    &&  find content/pages -type f -name "*.adoc" -exec sed -i 's|:phrase|:page-phrase|g' {} + \
    &&  find content/pages -type f -name "*.adoc" -exec sed -i 's|:slug|:page-slug|g' {} + \
    &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:description|:page-description|g" {} + \
    &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:keywords|:page-keywords|g" {} + \
    &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:definition:|:page-definition:|g" {} + \
    &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:banner|:page-banner|g" {} + \
    &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:subtitle|:page-subtitle|g" {} + \
    &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:subtext|:page-subtext|g" {} + \
    &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|../theme/images|../images|g" {} + \
    &&  find content/blog -type f -name "*.adoc" -exec sed -i 's|:slug|:page-slug|g' {} + \
    &&  find content/blog -type f -name "*.adoc" -exec sed -i "s|:alt|:page-alt|g" {} + \
    &&  find content/blog -type f -name "*.adoc" -exec sed -i "s|:author|:page-author|g" {} + \
    &&  find content/blog -type f -name "*.adoc" -exec sed -i "s|:date|:page-date|g" {} + \
    &&  find content/blog -type f -name "*.adoc" -exec sed -i "s|:description|:page-description|g" {} + \
    &&  find content/blog -type f -name "*.adoc" -exec sed -i "s|:image|:page-image|g" {} + \
    &&  find content/blog -type f -name "*.adoc" -exec sed -i "s|:keywords|:page-keywords|g" {} + \
    &&  find content/blog -type f -name "*.adoc" -exec sed -i "s|:subtitle|:page-subtitle|g" {} + \
    &&  find content/blog -type f -name "*.adoc" -exec sed -i "s|:writer|:page-writer|g" {} + \
    &&  find content/blog -type f -name "*.adoc" -exec sed -i "s|:tags|:page-tags|g" {} + \
    &&  find content/blog -type f -name "*.adoc" -exec sed -i "s|:category|:page-category|g" {} + \
    &&  rm -rf content/pages/products \
    &&  copy __envAirsNpm__/node_modules 'node_modules' \
    &&  install_fontawesome_pro \
    &&  if test -n "${CI:-}" && test "${CI_COMMIT_REF_NAME}" != "master"
        then
          HOME=. ./node_modules/.bin/gatsby build --prefix-paths
        else
          HOME=. ./node_modules/.bin/gatsby build
        fi \
        &&  rm -rf content \
  &&  popd \
  ||  return 1
}

main "${@}"
