# shellcheck shell=bash

function main {
  local src="${1}"
  local action="${2}"

  export NODE_OPTIONS=--max-old-space-size=4096
  : \
    && aws_login "dev" "3600" \
    && sops_export_vars __argAirsSecrets__/dev.yaml \
      CLOUDINARY_API_SECRET \
      CLOUDINARY_API_KEY \
      CLOUDINARY_CLOUD_NAME \
      GATSBY_ALGOLIA_APP_ID \
      GATSBY_ALGOLIA_SEARCH_KEY \
      ALGOLIA_ADMIN_KEY \
      GATSBY_AUTH0_DOMAIN \
      GATSBY_AUTH0_CLIENT_ID \
      GATSBY_AUTH0_CALLBACK \
    && pushd "${src}" \
    && rm -rf node_modules \
    && copy __argAirsNpm__ node_modules \
    && install_scripts \
    && popd \
    && npm run "${action}" --prefix airs/front/
}

main "${@}"
