# shellcheck shell=bash

declare -Arx SKIMS_GLOBAL_PKGS=(
  [cli]=skims/cli
  [config]=skims/config
  [core]=skims/core
  [integrates]=skims/integrates
  [lib_path]=skims/lib_path
  [nvd]=skims/nvd
  [parse_cfn]=skims/parse_cfn
  [parse_grammar]=skims/parse_grammar
  [parse_json]=skims/parse_json
  [serialization]=skims/serialization
  [state]=skims/state
  [utils]=skims/utils
  [zone]=skims/zone
)

declare -Arx SKIMS_GLOBAL_TEST_PKGS=(
  [test]=test/
)

function job_skims_doc {
      helper_common_poetry_install_deps skims \
  &&  pushd skims \
    &&  echo '[INFO] Building' \
    &&  rm -rf docs/skims/ \
    &&  poetry run pdoc \
          --force \
          --html \
          --output-dir docs/ \
          --template-dir docs/templates/ \
          skims \
  &&  popd \
  &&  rm -rf public/ \
  &&  git checkout -- public/ \
  &&  mv skims/docs/skims public/ \
  ||  return 1

}

function job_skims_deploy_infra {
      pushd skims \
    &&  helper_skims_aws_login prod \
    &&  helper_common_terraform_apply infra \
  &&  popd \
  ||  return 1
}

function job_skims_deploy_to_pypi {
  # Propagated from Gitlab env vars
  export SKIMS_PYPI_TOKEN
  local version

  function restore_version {
    sed --in-place 's|^version.*$|version = "1.0.0"|g' "skims/pyproject.toml"
  }

      helper_skims_compile_ast \
  &&  helper_common_poetry_install_deps skims \
  &&  pushd skims \
    &&  version=$(helper_skims_compute_version) \
    &&  echo "[INFO] Skims: ${version}" \
    &&  trap 'restore_version' EXIT \
    &&  sed --in-place \
          "s|^version = .*$|version = \"${version}\"|g" \
          'pyproject.toml' \
    &&  poetry publish \
          --build \
          --password "${PYPI_TOKEN}" \
          --username '__token__' \
  &&  popd \
  ||  return 1
}

function job_skims_install {
      helper_skims_compile_ast \
  &&  helper_common_poetry_install skims \

}

function job_skims_lint {
  local args_mypy=(
    --config-file 'settings.cfg'
  )
  local args_prospector=(
    # Some day when skims has https://readthedocs.org !
    # --doc-warnings
    --full-pep8
    --strictness veryhigh
    --test-warnings
  )

      helper_common_poetry_install_deps skims \
  &&  pushd skims \
    &&  echo '[INFO] Checking static typing' \
    &&  poetry run mypy "${args_mypy[@]}" skims/ \
    &&  poetry run mypy "${args_mypy[@]}" test/ \
    &&  echo "[INFO] Linting" \
    &&  poetry run prospector "${args_prospector[@]}" skims/ \
    &&  poetry run prospector "${args_prospector[@]}" test/ \
  &&  popd \
  ||  return 1
}

function job_skims_security {
  local bandit_args=(
    --recursive skims/
  )

      helper_common_poetry_install_deps skims \
  &&  pushd skims \
    &&  poetry run bandit "${bandit_args[@]}" \
  &&  popd \
  ||  return 1
}

function job_skims_structure {
  local base_args=(
    --cluster
    --include-missing
    --max-bacon 0
    --noshow
    --only "${!SKIMS_GLOBAL_PKGS[@]}"
    --reverse
    -x 'click'
  )
  local end_args=(
    --
    "${SKIMS_GLOBAL_PKGS[cli]}"
  )

      helper_common_poetry_install_deps skims \
  &&  pushd skims \
    &&  echo "[INFO]: Running pydeps" \
    &&  poetry run pydeps -o skims.file-dag.svg "${base_args[@]}" \
          --max-cluster-size 100 \
          "${end_args[@]}" \
    &&  poetry run pydeps -o skims.module-dag.svg "${base_args[@]}" \
          --max-cluster-size 1 \
          "${end_args[@]}" \
    &&  poetry run pydeps -o skims.cycles.svg "${base_args[@]}" \
          --max-cluster-size 100 \
          --show-cycles \
          "${end_args[@]}" \
  &&  popd \
  ||  return 1
}

function job_skims_test {
  export PYTHONUNBUFFERED='1'
  local args_pytest=(
    --capture tee-sys
    --cov-branch
    --cov-report 'term'
    --cov-report "html:${PWD}/skims/coverage/"
    --cov-report "xml:${PWD}/skims/coverage.xml"
    --disable-pytest-warnings
    --exitfirst
    --no-cov-on-fail
    --reruns 2
    --show-capture no
    --verbose
  )

      helper_skims_compile_ast \
  &&  helper_common_poetry_install_deps skims \
  &&  pushd skims \
    &&  for pkg in "${SKIMS_GLOBAL_PKGS[@]}" "${SKIMS_GLOBAL_TEST_PKGS[@]}"
        do
          args_pytest+=( "--cov=${pkg}" )
        done \
    &&  poetry run pytest "${args_pytest[@]}" < /dev/null \
  &&  popd \
  ||  return 1
}

function job_skims_test_infra {
      pushd skims \
    &&  helper_skims_aws_login dev \
    &&  helper_common_terraform_plan infra \
  &&  popd \
  ||  return 1
}
