# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"

cat << EOF >> "${out}"
#! /usr/bin/env bash

source "${genericShellOptions}"

export genericShellOptions="${genericShellOptions}"

export srcFluidasserts="${srcFluidasserts}"
export srcSetupCfg="${srcSetupCfg}"
export srcTest="${srcTest}"

export pyPkgFluidassertsBasic="${pyPkgFluidassertsBasic}"
export pyPkgGroupTest="${pyPkgGroupTest}"

export fluidassertsModule="${testGroupName}"

echo 'Verifying inputs ...'
test -n "\${ENCRYPTION_KEY}" \
  && echo '  [OK] encryption key present' \
  || (
    echo '  [FAIL] encryption key not present, please export ENCRYPTION_KEY'
    exit 1
  )
echo

echo 'Unencrypting secrets and exporting them to the current context ...'
source <( \
  echo "\${ENCRYPTION_KEY}" \
    | ${gpg}/bin/gpg \
      --batch \
      --passphrase-fd 0 \
      --decrypt "${envVarsEncrypted}")
echo

echo "Creating an ephemeral test runner for ${testGroupName} ..."
cp --force "${runner}" "ephemeral-test-runner"
chmod +x "ephemeral-test-runner"
echo

echo "Executing tests for ${testGroupName} ..."
./ephemeral-test-runner
EOF
