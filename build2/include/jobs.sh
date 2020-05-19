# shellcheck shell=bash

source "${srcIncludeHelpers}"
source "${srcEnv}"

function job_build_nix_caches {
  local context='.'
  local dockerfile='build2/Dockerfile'
  local provisioners

      helper_use_pristine_workdir \
  &&  provisioners=(./build2/provisioners/*) \
  &&  helper_build_nix_caches_parallel \
  &&  for (( i="${lower_limit}";i<="${upper_limit}";i++ ))
      do
            provisioner=$(basename "${provisioners[${i}]}") \
        &&  provisioner="${provisioner%.*}" \
        &&  helper_docker_build_and_push \
              "${CI_REGISTRY_IMAGE}/nix:${provisioner}" \
              "${context}" \
              "${dockerfile}" \
              'PROVISIONER' "${provisioner}" \
        ||  return 1
      done
}

function job_lint_commit_message {
  local commit_diff
  local commit_hashes
  local parser_url='https://static-objects.gitlab.net/fluidattacks/public/raw/master/commitlint-configs/others/parser-preset.js'
  local rules_url='https://static-objects.gitlab.net/fluidattacks/public/raw/master/commitlint-configs/others/commitlint.config.js'

      helper_use_pristine_workdir \
  &&  curl -LOJ "${parser_url}" \
  &&  curl -LOJ "${rules_url}" \
  &&  npm install @commitlint/{config-conventional,cli} \
  &&  git fetch --prune > /dev/null \
  &&  if [ "${IS_LOCAL_BUILD}" = "${TRUE}" ]
      then
            commit_diff="origin/master..${CI_COMMIT_REF_NAME}"
      else
            commit_diff="origin/master..origin/${CI_COMMIT_REF_NAME}"
      fi \
  &&  commit_hashes="$(git log --pretty=%h "${commit_diff}")" \
  &&  for commit_hash in ${commit_hashes}
      do
            git log -1 --pretty=%B "${commit_hash}" | npx commitlint \
        ||  return 1
      done
}

function job_lint_shell {
  local path_to_check='build2'

      echo "Verifying shell code in: ${path_to_check}" \
  &&  find "${path_to_check}" -name '*.sh' \
        -exec shellcheck --exclude=SC1090,SC2154,SC2164,SC2064 -x {} + \
  &&  shellcheck -x --exclude=SC2015,SC2064 ./build2.sh
}

function job_lint_nix {
  local path_to_check='build2'

      echo "Verifying nix code in: ${path_to_check}" \
  &&  nix-linter \
        --check=DIYInherit \
        --check=EmptyInherit \
        --check=EmptyLet \
        --check=EtaReduce \
        --check=FreeLetInFunc \
        --check=LetInInheritRecset \
        --check=ListLiteralConcat \
        --check=NegateAtom \
        --check=SequentialLet \
        --check=SetLiteralUpdate \
        --check=UnfortunateArgName \
        --check=UnneededRec \
        --check=UnusedArg \
        --check=UnusedLetBind \
        --check=UpdateEmptySet \
        --check=BetaReduction \
        --check=EmptyVariadicParamSet \
        --check=UnneededAntiquote \
        --recursive \
        "${path_to_check}"
}

function job_lint_asserts {
  local config_file='.pylintrc'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_config_precommit \
  &&  helper_list_touched_files | xargs pre-commit run -v --files \
  &&  prospector \
        --full-pep8 \
        --without-tool pep257 \
        --with-tool pyroma \
        --strictness veryhigh \
        --output-format text \
        --pylint-config-file="${config_file}" \
        fluidasserts/
}

function job_lint_asserts_bandit {
      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  bandit \
        -ii \
        -s B501,B601,B402,B105,B321,B102,B107,B307 \
        -r \
        fluidasserts
}

function job_lint_asserts_tests {
  local config_file='.pylintrc'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_config_precommit \
  &&  helper_list_touched_files | xargs pre-commit run -v --files \
  &&  prospector \
        --full-pep8 \
        --without-tool pep257 \
        --with-tool pyroma \
        --strictness veryhigh \
        --output-format text \
        --pylint-config-file="${config_file}" \
        test/
}

function job_send_new_release_email {
  export MANDRILL_EMAIL_TO='engineering@fluidattacks.com'

      env_prepare_python_packages \
  &&  helper_with_production_secrets \
  &&  curl -Lo \
        "${TEMP_FILE1}" \
        'https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/mail.py' \
  &&  echo "send_mail('new_version', MANDRILL_EMAIL_TO,
        context={'project': PROJECT, 'project_url': '${CI_PROJECT_URL}',
          'version': _get_version_date(), 'message': _get_message()},
        tags=['general'])" >> "${TEMP_FILE1}" \
  &&  python3 "${TEMP_FILE1}"
}

function job_test_asserts_api_cloud_aws_api {
  local marker_name='cloud_aws_api'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_cloud_aws_cloudformation {
  local marker_name='cloud_aws_cloudformation'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_cloud_aws_terraform {
  local marker_name='cloud_aws_terraform'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_cloud_azure {
  local marker_name='cloud_azure'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_cloud_gcp {
  local marker_name='cloud_gcp'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_cloud_kubernetes {
  local marker_name='cloud_kubernetes'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_db_mssql {
  local marker_name='db_mssql'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_db_mysql {
  local marker_name='db_mysql'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_db_postgres {
  local marker_name='db_postgres'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_format {
  local marker_name='format'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_helper {
  local marker_name='helper'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_iot {
  local marker_name='iot'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_core {
  local marker_name='lang_core'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_csharp {
  local marker_name='lang_csharp'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_docker {
  local marker_name='lang_docker'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_dotnetconfig {
  local marker_name='lang_dotnetconfig'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_html {
  local marker_name='lang_html'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_java {
  local marker_name='lang_java'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_javascript {
  local marker_name='lang_javascript'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_php {
  local marker_name='lang_php'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_python {
  local marker_name='lang_python'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_rpgle {
  local marker_name='lang_rpgle'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_lang_times {
  local marker_name='lang_times'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_ot {
  local marker_name='ot'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_proto_dns {
  local marker_name='proto_dns'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_proto_ftp {
  local marker_name='proto_ftp'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_proto_git {
  local marker_name='proto_git'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_proto_graphql {
  local marker_name='proto_graphql'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_proto_http {
  local marker_name='proto_http'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_proto_ldap {
  local marker_name='proto_ldap'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_proto_rest {
  local marker_name='proto_rest'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_proto_smb {
  local marker_name='proto_smb'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_proto_smtp {
  local marker_name='proto_smtp'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_proto_ssh {
  local marker_name='proto_ssh'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_proto_ssl {
  local marker_name='proto_ssl'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_proto_tcp {
  local marker_name='proto_tcp'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_sca {
  local marker_name='sca'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_syst {
  local marker_name='syst'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}

function job_test_asserts_api_utils {
  local marker_name='utils'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  helper_test_fluidasserts "${marker_name}"
}
