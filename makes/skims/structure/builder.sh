# shellcheck shell=bash

source "${makeDerivation}"
source "${envBashLibPython}"

function main {
      echo '[INFO] Creating a staging area' \
  &&  copy "${envSrcSkimsSkims}" "${PWD}/skims" \
  &&  pkgs=( $(ls -1  "${envSrcSkimsSkims}") ) \
  &&  echo "[INFO] Packages: ${pkgs[@]}" \
  &&  base_args=(
        --cluster
        --include-missing
        --max-bacon 0
        --only "${pkgs[@]}"
        --noshow
        --reverse
        -x 'click'
      ) \
  &&  end_args=(
        --
        'skims/cli'
      ) \
  &&  make_python_path \
        "${envPythonRequirementsDevelopment}" \
        "${envPythonRequirementsRuntime}" \
  &&  make_python_path_plain \
        "${envSrcSkimsSkims}" \
        "${PWD}" \
  &&  echo '[INFO] Creating images' \
  &&  pydeps -o file.svg "${base_args[@]}" \
        --max-cluster-size 100 \
        "${end_args[@]}" \
  &&  pydeps -o module.svg "${base_args[@]}" \
        --max-cluster-size 1 \
        "${end_args[@]}" \
  &&  pydeps -o cycles.svg "${base_args[@]}" \
        --max-cluster-size 100 \
        --show-cycles \
        "${end_args[@]}" \
  &&  mkdir "${out}" \
  &&  mv "${PWD}/"*'.svg' "${out}"
}

main "${@}"
