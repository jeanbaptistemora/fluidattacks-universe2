# shellcheck shell=bash

function main {
  local src='makes/applications/makes/doc/src'
  local bucket
  export env="${1}"
  export CI_COMMIT_REF_NAME

      if [ "${env}" = 'prod' ]
      then
        bucket='s3://doc.fluidattacks.com/'
      elif [ "${env}" = 'dev' ]
      then
        bucket="s3://doc-dev.fluidattacks.com/${CI_COMMIT_REF_NAME}/"
      else
            echo '[ERROR] Either "prod" or "dev" must be passed as arg' \
        &&  return 1
      fi \
  &&  pushd "${src}" \
    &&  "aws_login_${env}" serves \
    &&  copy "__envRuntime__/node_modules" node_modules \
    &&  chmod +x node_modules/.bin/* \
    &&  npm run build \
    &&  aws s3 sync build "${bucket}" --delete \
    &&  rm -rf node_modules build .docusaurus \
  &&  popd \
  ||  return 1
}

main "${@}"
