# shellcheck shell=bash

function main {
  export LANG=en_US.UTF-8
  local secrets=(PLAYSTORE_CREDENTIALS)
  local files=(
    'integrates/mobile/app.json'
    'integrates/mobile/assets/icon.png'
    'integrates/mobile/assets/splash.png'
  )

  if has_any_file_changed "${files[@]}"; then
    echo '[INFO] Logging in to AWS...' \
      && aws_login_prod_new integrates \
      && sops_export_vars __argSecretsProd__ "${secrets[@]}" \
      && pushd integrates/mobile \
      && echo "${PLAYSTORE_CREDENTIALS}" > playstore-credentials.json \
      && bundle exec fastlane supply \
        --aab ./output/asm.aab \
        --json_key ./playstore-credentials.json \
        --package_name "com.fluidattacks.integrates" \
        --track production \
      && rm -rf playstore-credentials.json \
      && popd \
      || return 1
  else
    echo '[INFO] No relevant files were modified, skipping deploy' \
      && return 0
  fi
}

main "${@}"
