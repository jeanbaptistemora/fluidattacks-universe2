# shellcheck shell=bash


function main {
  local url='https://please-replace-me-before-deploying'
  local path='/please-replace-me-before-deploying'

      copy "${envAirsNewFront}" new-front \
  &&  copy "${envAirsContent}" content \
  &&  sed -i "s|https://fluidattacks.com/new-front|${url}|g" new-front/gatsby-config.js \
  &&  sed -i "s|pathPrefix: '/new-front'|pathPrefix: '${path}'|g" new-front/gatsby-config.js \
  &&  find content/pages -type f -name "*.adoc" -exec sed -i 's|:slug|:page-slug|g' {} + \
  &&  rm -rf \
        content/pages/about-us/clients \
        content/pages/products/defends \
        content/pages/products/rules \
  &&  pushd new-front \
    &&  copy "${envAirsNpm}/node_modules" 'node_modules' \
    &&  chmod +x ./node_modules/.bin/gatsby \
    &&  HOME=. ./node_modules/.bin/gatsby build --prefix-paths \
    &&  mkdir "${out}" \
    &&  copy public "${out}" \
  &&  popd \
  ||  return 1
}

main "${@}"
