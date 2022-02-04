# shellcheck shell=bash

function main {
  local src="${1}"

  aws_login_dev \
    && sops_export_vars __argAirsSecrets__/dev.yaml \
      CLOUDINARY_API_SECRET \
      CLOUDINARY_API_KEY \
      CLOUDINARY_CLOUD_NAME \
      GATSBY_ALGOLIA_APP_ID \
      GATSBY_ALGOLIA_SEARCH_KEY \
      ALGOLIA_ADMIN_KEY \
    && pushd "${src}" \
    && copy __argAirsNpm__ 'node_modules' \
    && popd \
    && npm run develop --prefix airs/front/
}

main "${@}"
