# shellcheck shell=bash

source "${makeDerivation}"
source "${envSetupSkimsDevelopment}"
source "${envSetupSkimsRuntime}"

function list_packages {
      target="${PWD}/test" \
  &&  copy "${envSrcSkimsTest}" "${target}" \
  &&  echo "${target}" \
  &&  find "${envSrcSkimsSkims}" -mindepth 1 -maxdepth 1 -type d \
        | while read -r folder
          do
                target="${PWD}/$(basename "${folder}")" \
            &&  copy "${folder}" "${target}" \
            &&  echo "${target}" \
            ||  return 1
          done
}

function main {
  local pkgs

      pkgs=$(mktemp) \
  &&  list_packages > "${pkgs}" \
  &&  while read -r pkg
      do
            pkg_dir="$(dirname "${pkg}")" \
        &&  pkg_name="$(basename "${pkg}")" \
        &&  echo "[INFO] Running mypy over: ${pkg}" \
        &&  pushd "${pkg_dir}" \
          &&  mypy \
                --config-file "${envSrcSkimsSettingsCfg}" \
                "${pkg_name}" \
        &&  popd \
        ||  return 1
      done < "${pkgs}" \
  &&  while read -r pkg
      do
            pkg_dir="$(dirname "${pkg}")" \
        &&  pkg_name="$(basename "${pkg}")" \
        &&  echo "[INFO] Running prospector over: ${pkg}" \
        &&  prospector \
              --full-pep8 \
              --profile "${envSrcSkimsProspectorProfile}" \
              --strictness 'veryhigh' \
              --test-warnings \
              "${pkg}" \
        ||  return 1
      done < "${pkgs}" \
  &&  success
}

main "${@}"
