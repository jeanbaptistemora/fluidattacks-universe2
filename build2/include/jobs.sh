# shellcheck shell=bash

source "${srcIncludeHelpers}"
source "${srcExternalSops}"
source "${srcExternalGitlabVariables}"
source "${srcEnv}"

function job_build_nix_caches {
  local provisioners
  local dockerfile
  local context='.'
  local dockerfile='build/Dockerfile'

      helper_use_pristine_workdir \
  &&  provisioners=(./build/provisioners/*) \
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

function job_test_infra_autoscaling_ci {
  local target='services/autoscaling-ci/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_infra_autoscaling_ci {
  local target='services/autoscaling-ci/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_test_infra_analytics {
  local target='services/analytics/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_infra_analytics {
  local target='services/analytics/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_test_infra_aws_sso {
  local target='services/aws-sso/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_infra_aws_sso {
  local target='services/aws-sso/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_test_infra_fluid_vpc {
  local target='services/fluid-vpc/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_infra_fluid_vpc {
  local target='services/fluid-vpc/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_test_infra_secret_management {
  local target='secret-management/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_infra_secret_management {
  local target='secret-management/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_test_user_provision_asserts_dev {
  local target='services/user-provision/asserts/dev/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_user_provision_asserts_dev {
  local target='services/user-provision/asserts/dev/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_test_user_provision_asserts_prod {
  local target='services/user-provision/asserts/prod/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_user_provision_asserts_prod {
  local target='services/user-provision/asserts/prod/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_test_user_provision_services_dev {
  local target='services/user-provision/services/dev/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_user_provision_services_dev {
  local target='services/user-provision/services/dev/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_test_user_provision_services_prod {
  local target='services/user-provision/services/prod/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_user_provision_services_prod {
  local target='services/user-provision/services/prod/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_test_user_provision_integrates_dev {
  local target='services/user-provision/integrates/dev/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_user_provision_integrates_dev {
  local target='services/user-provision/integrates/dev/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_test_user_provision_integrates_prod {
  local target='services/user-provision/integrates/prod/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_user_provision_integrates_prod {
  local target='services/user-provision/integrates/prod/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_test_user_provision_web_dev {
  local target='services/user-provision/web/dev/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_user_provision_web_dev {
  local target='services/user-provision/web/dev/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_test_user_provision_web_prod {
  local target='services/user-provision/web/prod/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_plan \
        "${target}"
}

function job_apply_user_provision_web_prod {
  local target='services/user-provision/web/prod/terraform'

      helper_use_pristine_workdir \
  &&  helper_terraform_apply \
        "${target}"
}

function job_apply_rotate_keys_user_provision_asserts_dev {
  local terraform_dir='services/user-provision/asserts/dev/terraform'
  local resource_to_taint='aws_iam_access_key.asserts-dev-key'
  local output_key_id_name='asserts-dev-secret-key-id'
  local output_secret_key_name='asserts-dev-secret-key'
  local gitlab_repo_id='4593516'
  local gitlab_key_id_name='DEV_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='DEV_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='false'

      helper_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}"
}

function job_apply_rotate_keys_user_provision_asserts_prod {
  local terraform_dir='services/user-provision/asserts/prod/terraform'
  local resource_to_taint='aws_iam_access_key.asserts-prod-key'
  local output_key_id_name='asserts-prod-secret-key-id'
  local output_secret_key_name='asserts-prod-secret-key'
  local gitlab_repo_id='4593516'
  local gitlab_key_id_name='PROD_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='PROD_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='true'

      helper_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}"
}

function job_apply_rotate_keys_user_provision_services_dev {
  local terraform_dir='services/user-provision/services/dev/terraform'
  local resource_to_taint='aws_iam_access_key.continuous-dev-key'
  local output_key_id_name='continuous-dev-secret-key-id'
  local output_secret_key_name='continuous-dev-secret-key'
  local gitlab_repo_id='4603023'
  local gitlab_key_id_name='DEV_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='DEV_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='false'

      helper_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}"
}

function job_apply_rotate_keys_user_provision_services_prod {
  local terraform_dir='services/user-provision/services/prod/terraform'
  local resource_to_taint='aws_iam_access_key.continuous-prod-key'
  local output_key_id_name='continuous-prod-secret-key-id'
  local output_secret_key_name='continuous-prod-secret-key'
  local gitlab_repo_id='4603023'
  local gitlab_key_id_name='PROD_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='PROD_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='true'

      helper_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}"
}

function job_apply_rotate_keys_user_provision_integrates_dev {
  local terraform_dir='services/user-provision/integrates/dev/terraform'
  local resource_to_taint='aws_iam_access_key.integrates-dev-key'
  local output_key_id_name='integrates-dev-secret-key-id'
  local output_secret_key_name='integrates-dev-secret-key'
  local gitlab_repo_id='4620828'
  local gitlab_key_id_name='DEV_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='DEV_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='false'

      helper_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}"
}

function job_apply_rotate_keys_user_provision_integrates_prod {
  local terraform_dir='services/user-provision/integrates/prod/terraform'
  local resource_to_taint='aws_iam_access_key.integrates-prod-key'
  local output_key_id_name='integrates-prod-secret-key-id'
  local output_secret_key_name='integrates-prod-secret-key'
  local gitlab_repo_id='4620828'
  local gitlab_key_id_name='PROD_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='PROD_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='true'

      helper_check_last_job_succeeded \
        "${gitlab_repo_id}" \
        'deploy_k8s_back' \
  &&  helper_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}" \
  &&  helper_deploy_integrates
}

function job_apply_rotate_keys_user_provision_web_dev {
  local terraform_dir='services/user-provision/web/dev/terraform'
  local resource_to_taint='aws_iam_access_key.web-dev-key'
  local output_key_id_name='web-dev-secret-key-id'
  local output_secret_key_name='web-dev-secret-key'
  local gitlab_repo_id='4649627'
  local gitlab_key_id_name='DEV_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='DEV_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='false'

      helper_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}"
}

function job_apply_rotate_keys_user_provision_web_prod {
  local terraform_dir='services/user-provision/web/prod/terraform'
  local resource_to_taint='aws_iam_access_key.web-prod-key'
  local output_key_id_name='web-prod-secret-key-id'
  local output_secret_key_name='web-prod-secret-key'
  local gitlab_repo_id='4649627'
  local gitlab_key_id_name='PROD_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='PROD_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='true'

      helper_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}"
}

function job_test_commit_msg {
      helper_use_pristine_workdir \
  &&  env_prepare_node_modules \
  &&  helper_test_commit_msg_commitlint
}

function job_send_new_release_email {
  local temp

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  temp="$(mktemp)" \
  &&  trap 'rm -rf ${temp}' 'EXIT' \
  &&  helper_aws_login \
  &&  sops_env secrets-prod.yaml default \
        MANDRILL_APIKEY \
        MANDRILL_EMAIL_TO \
  &&  curl -Lo \
        "${temp}" \
        'https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/mail.py' \
  &&  echo "send_mail('new_version', MANDRILL_EMAIL_TO,
        context={'project': PROJECT, 'project_url': '${CI_PROJECT_URL}',
          'version': _get_version_date(), 'message': _get_message()},
        tags=['general'])" >> "${temp}" \
  &&  python3 "${temp}"
}
