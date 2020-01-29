# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"

cat << EOF >> "${out}"
#! /usr/bin/env bash

source "${genericShellOptions}"

export genericShellOptions="${genericShellOptions}"

export srcEnvVarsProdEncrypted="${srcEnvVarsProdEncrypted}"

export buildFluidassertsRelease="${buildFluidassertsRelease}"

echo 'Verifying inputs ...'
test -n "\${ENCRYPTION_KEY_PROD:-}" \
  && echo '  [OK] production encryption key present' \
  || (
    echo '  [FAIL] production encryption key not present, please export ENCRYPTION_KEY'
    exit 1
  )
echo

echo 'Unencrypting secrets and exporting them to the current context ...'
source <( \
  echo "\${ENCRYPTION_KEY_PROD}" \
    | ${gpg}/bin/gpg \
      --batch \
      --passphrase-fd 0 \
      --decrypt "${srcEnvVarsProdEncrypted}")
echo

echo "Creating an ephemeral test runner ..."
cp --force "${runner}" "ephemeral-runner"
chmod +x "ephemeral-runner"
echo

echo "Executing ephemeral runner ..."
./ephemeral-runner
EOF
