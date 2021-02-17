# shellcheck shell=bash

function main {
  local commit_diff
  local commit_hashes
  export CI
  export CI_COMMIT_REF_NAME

      git fetch --prune > /dev/null \
  &&  if test -n "${CI:-}"
      then
        commit_diff="origin/master..origin/${CI_COMMIT_REF_NAME}"
      else
        commit_diff="origin/master..${CI_COMMIT_REF_NAME}"
      fi \
  &&  commit_hashes="$(git log --pretty=%h "${commit_diff}")" \
  &&  for commit_hash in ${commit_hashes}
      do
            git log -1 --pretty=%B "${commit_hash}" | commitlint \
        ||  return 1
      done
}

main "${@}"
