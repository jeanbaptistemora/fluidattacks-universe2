# shellcheck shell=bash

function main {
      copy "${envIntegratesBackModules}" "${PWD}/modules" \
  &&  ls -1 "${envIntegratesBackModules}" > list \
  &&  mapfile -t pkgs < list \
  &&  echo "[INFO] Packages: ${pkgs[*]}" \
  &&  base_args=(
        --cluster
        --include-missing
        --max-bacon 0
        --only "${pkgs[@]}"
        --noshow
        --reverse
      ) \
  &&  end_args=(
        --
        'modules/events'
      ) \
  &&  echo "Current working directory: ${PWD}" \
  &&  echo "Content: $(ls modules)" \
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
