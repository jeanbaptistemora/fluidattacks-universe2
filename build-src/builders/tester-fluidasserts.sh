# shellcheck shell=bash

source "${stdenv}/setup"

cat << EOF >> "${out}"
export stdenv="${stdenv}"
export genericDirs="${genericDirs}"
export genericShellOptions="${genericShellOptions}"

export srcFluidasserts="${srcFluidasserts}"
export srcSetupCfg="${srcSetupCfg}"
export srcTest="${srcTest}"

export pyPkgFluidasserts="${pyPkgFluidasserts}"
export pyPkgGroupTest="${pyPkgGroupTest}"

export fluidassertsModule="${testGroupName}"

echo 'Unencrypting secrets and exporting them to the current context ...'
source <(${gpg}/bin/gpg -d ${envVarsEncrypted})

echo "Creating an ephemeral test runner for ${testGroupName} ..."
cp --force "${runner}" "ephemeral-test-runner"
chmod +x "ephemeral-test-runner"
./ephemeral-test-runner
EOF
