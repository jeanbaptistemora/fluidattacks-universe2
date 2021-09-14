# shellcheck shell=bash

function main {
  local out="airs/front"

  pushd "${out}" \
    && aws_login_dev airs \
    && sops_export_vars __envAirsSecrets__/dev.yaml \
      CLOUDINARY_API_SECRET \
      CLOUDINARY_API_KEY \
      CLOUDINARY_CLOUD_NAME \
      FONTAWESOME_NPM_AUTH_TOKEN \
      GATSBY_ALGOLIA_APP_ID \
      GATSBY_ALGOLIA_SEARCH_KEY \
      ALGOLIA_ADMIN_KEY \
    && if test -n "${CI:-}" && test "${CI_COMMIT_REF_NAME}" != "master"; then
      sed -i "s|pathPrefix: '/front'|pathPrefix: '/${CI_COMMIT_REF_NAME}'|g" gatsby-config.js \
        && sed -i "s|https://fluidattacks.com|https://web.eph.fluidattacks.com/${CI_COMMIT_REF_NAME}|g" gatsby-config.js
    fi \
    && copy __envAirsNpm__ 'node_modules' \
    && install_scripts \
    && install_fontawesome_pro "" \
    && if test -n "${CI:-}" && test "${CI_COMMIT_REF_NAME}" != "master"; then
      npm run build:eph
    else
      npm run build
    fi \
    && find content/ -name "*.adoc" -type f -delete \
    && find content/ -type d -empty -delete \
    && mv content/pages/advisories/ content/ \
    && mv content/pages/careers/ content/ \
    && copy content public \
    && rm -rf content \
    && popd \
    || return 1
}

main "${@}"
