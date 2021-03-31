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
        --only "${pkgs[@]}" main
        --noshow
        --reverse
      ) \
  &&  pushd modules \
    &&  find . -wholename '*.py' \
          | sed -E 's|/__init__||g' \
          | sed -E 's|.py||g' \
          | sed -E 's|/|.|g' \
          | sed -E 's|^..|import |g' \
          > main.py \
    &&  end_args=(
          --
          main.py
        ) \
    &&  echo "Current working directory: ${PWD}" \
    &&  echo '[INFO] Creating file graph' \
    &&  pydeps -o file.svg "${base_args[@]}" \
          --max-cluster-size 100 \
          "${end_args[@]}" \
    &&  echo '[INFO] Creating module graph' \
    &&  pydeps -o module.svg "${base_args[@]}" \
          --max-cluster-size 1 \
          "${end_args[@]}" \
    &&  echo '[INFO] Creating cycles graph' \
    &&  pydeps -o cycles.svg "${base_args[@]}" \
          --max-cluster-size 100 \
          --show-cycles \
          "${end_args[@]}" \
    &&  mkdir "${out}" \
    &&  mv "${PWD}/"*'.svg' "${out}" \
  &&  popd \
  ||  return 1
}

main "${@}"
