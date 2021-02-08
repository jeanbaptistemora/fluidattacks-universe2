# shellcheck shell=bash

source '__envSearchPaths__'
source '__envUtilsCommon__'

function main {
  local commitlint='node_modules/@commitlint/cli/cli.js'
  local commit_diff
  local commit_hashes
  export CI
  export CI_COMMIT_REF_NAME

      copy "__envSetupCommitlint__/node_modules" node_modules \
  &&  chmod +x "${commitlint}" \
  &&  git fetch --prune > /dev/null \
  &&  if test -n "${CI:-}"
      then
        commit_diff="origin/master..origin/${CI_COMMIT_REF_NAME}"
      else
        commit_diff="origin/master..${CI_COMMIT_REF_NAME}"
      fi \
  &&  commit_hashes="$(git log --pretty=%h "${commit_diff}")" \
  &&  for commit_hash in ${commit_hashes}
      do
            git log -1 --pretty=%B "${commit_hash}" | ./"${commitlint}" \
        ||  return 1
      done \
  &&  rm -rf node_modules
}

main
