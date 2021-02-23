# shellcheck shell=bash

function main {
  local src='makes/applications/makes/doc/src'
  local bucket='s3://doc.fluidattacks.com/'

      pushd "${src}" \
    &&  aws_login_prod serves \
    &&  copy "__envRuntime__/node_modules" node_modules \
    &&  chmod +x node_modules/.bin/* \
    &&  npm run build \
    &&  aws s3 sync build "${bucket}" --delete \
    &&  rm -rf node_modules build .docusaurus \
  &&  popd \
  ||  return 1
}

main "${@}"
