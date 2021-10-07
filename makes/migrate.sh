#! /usr/bin/env bash

function main {
  local path="${1}"

  sed -Ei 's/(\,|\{) makes/\1 inputs/g' "${path}"
  sed -Ei 's/(\,|\{) nixpkgs/\1 inputs/g' "${path}"
  sed -Ei 's/(\,|\{) packages/\1 inputs/g' "${path}"
  sed -Ei 's/(\,|\{) path/\1 projectPath/g' "${path}"
  sed -Ei 's|packages\.|inputs.product.|g' "${path}"
  sed -Ei 's|nixpkgs\.|inputs.nixpkgs.|g' "${path}"
  sed -Ei 's|makeEntrypoint|makeScript|g' "${path}"
  sed -Ei 's|arguments|replace|g' "${path}"
  # sed -Ei 's|arguments|env|g' "${path}"
  sed -Ei 's|envPaths|bin|g' "${path}"
  sed -Ei 's|envSources|source|g' "${path}"
  sed -Ei 's|path "/makes/applications/(.*)"|projectPath "/makes/foss/units/\1"|g' "${path}"
  sed -Ei 's|path "(.*)"|projectPath "\1"|g' "${path}"
  sed -Ei 's|"/makes/utils/(.*)"|(inputs.legacy.importUtility "\1")|g' "${path}"
  sed -Ei 's|envUtils = |source =|g' "${path}"
  sed -Ei 's|env([A-z].*) = |__arg\1__ =|g' "${path}"
  sed -Ei 's|env([A-z].*)|arg\1|g' "${path}"
  sed -Ei 's|makes\.||g' "${path}"
}

main "${@}"
