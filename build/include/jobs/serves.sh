# shellcheck shell=bash

source "${srcEnv}"
source "${srcIncludeHelpersCommon}"
source "${srcExternalGitlabVariables}"
source "${srcExternalSops}"
source "${srcIncludeHelpersServes}"

function job_serves_test_infra_monolith {
      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_infra_monolith 'test' \
  &&  popd \
  ||  return 1
}

function job_serves_apply_infra_monolith {
      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_infra_monolith 'deploy' \
  &&  popd \
  ||  return 1
}

function job_serves_test_infra_dns {
  local target='services/dns/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login dev \
  &&  helper_serves_infra_dns_get_load_balancer \
  &&  helper_common_terraform_plan \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_apply_infra_dns {
  local target='services/dns/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login prod \
  &&  helper_serves_infra_dns_get_load_balancer \
  &&  helper_common_terraform_apply \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_test_infra_autoscaling_ci {
  local target='services/autoscaling-ci/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login dev \
  &&  helper_common_terraform_plan \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_apply_infra_autoscaling_ci {
  local target='services/autoscaling-ci/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login prod \
  &&  helper_common_terraform_apply \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_test_infra_aws_sso {
  local target='services/aws-sso/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login dev \
  &&  helper_common_terraform_plan \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_apply_infra_aws_sso {
  local target='services/aws-sso/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login prod \
  &&  helper_common_terraform_apply \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_test_infra_fluid_vpc {
  local target='services/fluid-vpc/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login dev \
  &&  helper_common_terraform_plan \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_apply_infra_fluid_vpc {
  local target='services/fluid-vpc/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login prod \
  &&  helper_common_terraform_apply \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_test_infra_secret_management {
  local target='secret-management/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login dev \
  &&  helper_common_terraform_plan \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_apply_infra_secret_management {
  local target='secret-management/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login prod \
  &&  helper_common_terraform_apply \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_test_infra_certificates {
  local target='services/certificates/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login dev \
  &&  helper_common_terraform_plan \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_apply_infra_certificates {
  local target='services/certificates/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login prod \
  &&  helper_common_terraform_apply \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_test_user_provision_asserts_dev {
  local target='services/user-provision/asserts/dev/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login dev \
  &&  helper_common_terraform_plan \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_apply_user_provision_asserts_dev {
  local target='services/user-provision/asserts/dev/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login prod \
  &&  helper_common_terraform_apply \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_test_user_provision_asserts_prod {
  local target='services/user-provision/asserts/prod/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login dev \
  &&  helper_common_terraform_plan \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_apply_user_provision_asserts_prod {
  local target='services/user-provision/asserts/prod/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login prod \
  &&  helper_common_terraform_apply \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_test_user_provision_services_dev {
  local target='services/user-provision/services/dev/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login dev \
  &&  helper_common_terraform_plan \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_apply_user_provision_services_dev {
  local target='services/user-provision/services/dev/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login prod \
  &&  helper_common_terraform_apply \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_test_user_provision_services_prod {
  local target='services/user-provision/services/prod/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login dev \
  &&  helper_common_terraform_plan \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_apply_user_provision_services_prod {
  local target='services/user-provision/services/prod/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login prod \
  &&  helper_common_terraform_apply \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_test_user_provision_integrates_dev {
  local target='services/user-provision/integrates/dev/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login dev \
  &&  helper_common_terraform_plan \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_apply_user_provision_integrates_dev {
  local target='services/user-provision/integrates/dev/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login prod \
  &&  helper_common_terraform_apply \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_test_user_provision_integrates_prod {
  local target='services/user-provision/integrates/prod/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login dev \
  &&  helper_common_terraform_plan \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_apply_user_provision_integrates_prod {
  local target='services/user-provision/integrates/prod/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login prod \
  &&  helper_common_terraform_apply \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_test_user_provision_web_dev {
  local target='services/user-provision/web/dev/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login dev \
  &&  helper_common_terraform_plan \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_apply_user_provision_web_dev {
  local target='services/user-provision/web/dev/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login prod \
  &&  helper_common_terraform_apply \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_test_user_provision_web_prod {
  local target='services/user-provision/web/prod/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login dev \
  &&  helper_common_terraform_plan \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_apply_user_provision_web_prod {
  local target='services/user-provision/web/prod/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login prod \
  &&  helper_common_terraform_apply \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_test_user_provision_serves {
  local target='services/user-provision/serves/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login dev \
  &&  helper_common_terraform_plan \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_apply_user_provision_serves {
  local target='services/user-provision/serves/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login prod \
  &&  helper_common_terraform_apply \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_test_user_provision_observes {
  local target='services/user-provision/observes/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login dev \
  &&  helper_common_terraform_plan \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_apply_user_provision_observes {
  local target='services/user-provision/observes/terraform'

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_aws_login prod \
  &&  helper_common_terraform_apply \
        "${target}" \
  &&  popd \
  ||  return 1
}

function job_serves_rotate_keys_user_provision_asserts_dev {
  local terraform_dir='services/user-provision/asserts/dev/terraform'
  local resource_to_taint='aws_iam_access_key.asserts-dev-key'
  local output_key_id_name='asserts-dev-secret-key-id'
  local output_secret_key_name='asserts-dev-secret-key'
  local gitlab_repo_id='4593516'
  local gitlab_key_id_name='DEV_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='DEV_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='false'

      pushd serves \
  &&  helper_serves_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}" \
  &&  popd \
  ||  return 1
}

function job_serves_rotate_keys_user_provision_asserts_prod {
  local terraform_dir='services/user-provision/asserts/prod/terraform'
  local resource_to_taint='aws_iam_access_key.asserts-prod-key'
  local output_key_id_name='asserts-prod-secret-key-id'
  local output_secret_key_name='asserts-prod-secret-key'
  local gitlab_repo_id='4593516'
  local gitlab_key_id_name='PROD_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='PROD_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='true'

      pushd serves \
  &&  helper_serves_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}" \
  &&  popd \
  ||  return 1
}

function job_serves_rotate_keys_user_provision_services_dev {
  local terraform_dir='services/user-provision/services/dev/terraform'
  local resource_to_taint='aws_iam_access_key.continuous-dev-key'
  local output_key_id_name='continuous-dev-secret-key-id'
  local output_secret_key_name='continuous-dev-secret-key'
  local gitlab_repo_id='4603023'
  local gitlab_key_id_name='DEV_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='DEV_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='false'

      pushd serves \
  &&  helper_serves_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}" \
  &&  popd \
  ||  return 1
}

function job_serves_rotate_keys_user_provision_services_prod {
  local terraform_dir='services/user-provision/services/prod/terraform'
  local resource_to_taint='aws_iam_access_key.continuous-prod-key'
  local output_key_id_name='continuous-prod-secret-key-id'
  local output_secret_key_name='continuous-prod-secret-key'
  local gitlab_repo_id='4603023'
  local gitlab_key_id_name='PROD_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='PROD_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='true'

      pushd serves \
  &&  helper_serves_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}" \
  &&  popd \
  ||  return 1
}

function job_serves_rotate_keys_user_provision_integrates_dev {
  local terraform_dir='services/user-provision/integrates/dev/terraform'
  local resource_to_taint='aws_iam_access_key.integrates-dev-key'
  local output_key_id_name='integrates-dev-secret-key-id'
  local output_secret_key_name='integrates-dev-secret-key'
  local gitlab_repo_id='20741933'
  local gitlab_key_id_name='DEV_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='DEV_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='false'

      pushd serves \
  &&  helper_serves_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}" \
  &&  popd \
  ||  return 1
}

function job_serves_rotate_keys_user_provision_integrates_prod {
  local terraform_dir='services/user-provision/integrates/prod/terraform'
  local resource_to_taint='aws_iam_access_key.integrates-prod-key'
  local output_key_id_name='integrates-prod-secret-key-id'
  local output_secret_key_name='integrates-prod-secret-key'
  local gitlab_repo_id='20741933'
  local gitlab_key_id_name='PROD_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='PROD_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='true'

      pushd serves \
  &&  helper_serves_check_last_job_succeeded \
        "${gitlab_repo_id}" \
        'integrates_deploy_k8s_back' \
  &&  helper_serves_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}" \
  &&  helper_serves_deploy_integrates \
  &&  popd \
  ||  return 1
}

function job_serves_rotate_keys_user_provision_web_dev {
  local terraform_dir='services/user-provision/web/dev/terraform'
  local resource_to_taint='aws_iam_access_key.web-dev-key'
  local output_key_id_name='web-dev-secret-key-id'
  local output_secret_key_name='web-dev-secret-key'
  local gitlab_repo_id='4649627'
  local gitlab_key_id_name='DEV_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='DEV_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='false'

      pushd serves \
  &&  helper_serves_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}" \
  &&  popd \
  ||  return 1
}

function job_serves_rotate_keys_user_provision_web_prod {
  local terraform_dir='services/user-provision/web/prod/terraform'
  local resource_to_taint='aws_iam_access_key.web-prod-key'
  local output_key_id_name='web-prod-secret-key-id'
  local output_secret_key_name='web-prod-secret-key'
  local gitlab_repo_id='4649627'
  local gitlab_key_id_name='PROD_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='PROD_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='true'

      pushd serves \
  &&  helper_serves_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}" \
  &&  popd \
  ||  return 1
}

function job_serves_rotate_keys_user_provision_serves {
  local terraform_dir='services/user-provision/serves/terraform'
  local resource_to_taint='aws_iam_access_key.dev-key'
  local output_key_id_name='dev-secret-key-id'
  local output_secret_key_name='dev-secret-key'
  local gitlab_repo_id='20741933'
  local gitlab_key_id_name='SERVES_DEV_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='SERVES_DEV_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='false'

      pushd serves \
  &&  helper_serves_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}" \
  &&  popd \
  ||  return 1
}

function job_serves_rotate_keys_user_provision_observes {
  local terraform_dir='services/user-provision/observes/terraform'
  local gitlab_repo_id='20741933'

  # Dev
  local dev_resource_to_taint='aws_iam_access_key.dev-key'
  local dev_output_key_id_name='dev-secret-key-id'
  local dev_output_secret_key_name='dev-secret-key'
  local dev_gitlab_key_id_name='OBSERVES_DEV_AWS_ACCESS_KEY_ID'
  local dev_gitlab_secret_key_name='OBSERVES_DEV_AWS_SECRET_ACCESS_KEY'
  local dev_gitlab_masked='true'
  local dev_gitlab_protected='false'

  # Prod
  local prod_resource_to_taint='aws_iam_access_key.prod-key'
  local prod_output_key_id_name='prod-secret-key-id'
  local prod_output_secret_key_name='prod-secret-key'
  local prod_gitlab_key_id_name='OBSERVES_PROD_AWS_ACCESS_KEY_ID'
  local prod_gitlab_secret_key_name='OBSERVES_PROD_AWS_SECRET_ACCESS_KEY'
  local prod_gitlab_masked='true'
  local prod_gitlab_protected='true'

      pushd serves \
  &&  helper_serves_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${dev_resource_to_taint}" \
        "${dev_output_key_id_name}" \
        "${dev_output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${dev_gitlab_key_id_name}" \
        "${dev_gitlab_secret_key_name}" \
        "${dev_gitlab_masked}" \
        "${dev_gitlab_protected}" \
  &&  helper_serves_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${prod_resource_to_taint}" \
        "${prod_output_key_id_name}" \
        "${prod_output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${prod_gitlab_key_id_name}" \
        "${prod_gitlab_secret_key_name}" \
        "${prod_gitlab_masked}" \
        "${prod_gitlab_protected}" \
  &&  popd \
  ||  return 1
}

function job_serves_test_lint_code {

      helper_use_pristine_workdir \
  &&  pushd serves \
  &&  helper_serves_test_lint_code_shell . \
  &&  popd \
  ||  return 1
}

function job_serves_apply_config_autoscaling_ci {
  local bastion_ip='192.168.3.11'
  local bastion_user='ubuntu'
  local secrets_to_replace=(
    autoscaling_token_1
    autoscaling_token_2
    autoscaling_token_3
    autoscaling_token_4
    autoscaling_access_key
    autoscaling_secret_key
  )

      pushd serves \
  &&  echo '[INFO] Adding bastion to known hosts' \
  &&  helper_serves_aws_login prod \
  &&  mkdir -p ~/.ssh \
  &&  touch ~/.ssh/known_hosts \
  &&  ssh-keyscan \
        -H "${bastion_ip}" \
        >> ~/.ssh/known_hosts \
  &&  echo '[INFO] Exporting bastion SSH key' \
  &&  sops_env secrets-prod.yaml default \
        "${secrets_to_replace[@]}" \
        autoscaling_bastion_key_b64 \
  &&  echo -n "${autoscaling_bastion_key_b64}" \
        | base64 -d \
        > "${TEMP_FILE1}" \
  &&  echo '[INFO] Executing test: $ sudo whoami' \
  &&  ssh -i "${TEMP_FILE1}" "${bastion_user}@${bastion_ip}" \
        'sudo whoami' \
  &&  echo '[INFO] Writing config with secrets' \
  &&  cp './services/autoscaling-ci/config.toml' "${TEMP_FILE2}" \
  &&  for secret in "${secrets_to_replace[@]}"
      do
        rpl "__${secret}__" "${!secret}" "${TEMP_FILE2}" \
          |& grep 'Replacing' \
          |& sed -E 's/with.*$//g' \
          || return 1
      done \
  &&  echo '[INFO] Deploying config file to the bastion 1: /port/config.toml' \
  &&  scp -i "${TEMP_FILE1}" "${TEMP_FILE2}" "${bastion_user}@${bastion_ip}:/port/config.toml" \
  &&  echo '[INFO] Deploying config file to the bastion 2: /etc/gitlab-runner/config.toml' \
  &&  ssh -i "${TEMP_FILE1}" "${bastion_user}@${bastion_ip}" \
        'sudo mv /port/config.toml /etc/gitlab-runner/config.toml' \
  &&  echo '[INFO] Reloading config in the bastion from: /etc/gitlab-runner/config.toml' \
  &&  ssh -i "${TEMP_FILE1}" "${bastion_user}@${bastion_ip}" \
        'sudo killall -SIGHUP gitlab-runner' \
  &&  popd \
  ||  return 1
}
