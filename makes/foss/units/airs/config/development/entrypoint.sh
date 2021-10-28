# shellcheck shell=bash

function main {
  local src="${1}"

  aws_login_dev_new \
    && sops_export_vars __argAirsSecrets__/dev.yaml \
      CLOUDINARY_API_SECRET \
      CLOUDINARY_API_KEY \
      CLOUDINARY_CLOUD_NAME \
      FONTAWESOME_NPM_AUTH_TOKEN \
      GATSBY_ALGOLIA_APP_ID \
      GATSBY_ALGOLIA_SEARCH_KEY \
      ALGOLIA_ADMIN_KEY \
    && pushd "${src}" \
    && copy __argAirsNpm__ 'node_modules' \
    && install_scripts \
    && install_fontawesome_pro --no-save \
    && popd \
    && npm run develop --prefix airs/front/
}

main "${@}"
