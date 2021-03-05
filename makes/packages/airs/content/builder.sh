# shellcheck shell=bash

function main {
  local url='https://please-replace-this-url-before-deploying'
  local path='/please-replace-this-path-before-deploying'

      copy "${envAirsNewFront}" new-front \
  &&  copy "${envAirsContent}" content \
  &&  sed -i "s|https://fluidattacks.com/new-front|${url}|g" new-front/gatsby-config.js \
  &&  sed -i "s|pathPrefix: '/new-front'|pathPrefix: '${path}'|g" new-front/gatsby-config.js \
  &&  find content/pages -type f -name "*.adoc" -exec sed -i 's|:slug|:page-slug|g' {} + \
  &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:description|:page-description|g" {} + \
  &&  find content/pages -type f -name "*.adoc" -exec sed -i "s|:keywords|:page-keywords|g" {} + \
  &&  rm -rf \
        content/pages/about-us/clients \
        content/pages/products/defends \
        content/pages/products/rules \
  &&  pushd new-front \
    &&  copy "${envAirsNpm}/node_modules" 'node_modules' \
    &&  HOME=. ./node_modules/.bin/gatsby build --prefix-paths \
    &&  mkdir "${out}" \
    &&  copy public "${out}/new-front" \
  &&  popd \
  ||  return 1
}

main "${@}"
