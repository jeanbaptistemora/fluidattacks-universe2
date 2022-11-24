# shellcheck shell=bash

function main {
  local success=true
  local pytest_flags=()
  source __argExtraSrcs__/template extra_srcs

  : \
    && for extra_src in "${!extra_srcs[@]}"; do
      copy "${extra_srcs[$extra_src]}" "../${extra_src}"
    done \
    && pushd skims \
    && aws_login "dev" "3600" \
    && find skims -maxdepth 1 -type d -exec basename {} \; > modules.lst \
    && while read -r module; do
      pytest_flags+=("--cov=${module}")
    done < modules.lst \
    && if ! PYTHONPATH="${PWD}/skims:${PYTHONPATH}" pytest \
      "${pytest_flags[@]}" \
      --cov=test \
      --cov-branch \
      --cov-report=term \
      --reruns=1 \
      --skims-test-group=__argCategory__ \
      --capture=tee-sys \
      --disable-pytest-warnings \
      --durations=10 \
      --exitfirst \
      --showlocals \
      --show-capture=no \
      -vvv; then
      success=false
    fi \
    && mv .coverage .coverage.__argCategory__ \
    && popd \
    && if test "${success}" = false; then
      copy "${STATE}" .
      return 1
    fi
}

main "${@}"
