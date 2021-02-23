# shellcheck shell=bash

function main {
  export LANG=en_US.UTF-8
  local secrets=( PLAYSTORE_CREDENTIALS )

  if  has_any_file_changed \
    'integrates/mobile/app.json'
  then
        echo '[INFO] Logging in to AWS...' \
    &&  aws_login_prod integrates \
    &&  sops_export_vars __envSecretsProd__ "${secrets[@]}" \
    &&  pushd integrates/mobile \
      &&  echo "${PLAYSTORE_CREDENTIALS}" > playstore-credentials.json \
      &&  bundle exec fastlane supply \
            --aab ./output/integrates.aab \
            --json_key ./playstore-credentials.json \
            --package_name "com.fluidattacks.integrates" \
            --track production \
      &&  rm -rf playstore-credentials.json \
    &&  popd \
    ||  return 1
  else
        echo '[INFO] No relevant files were modified, skipping deploy' \
    &&  return 0
  fi
}

main "${@}"
