# shellcheck shell=bash

source "${srcIncludeHelpers}"
source "${srcExternalGitlabVariables}"
source "${srcExternalSops}"
source "${srcDotDotToolboxOthers}"

function job_deploy_docker_image_exams {
  local tag="registry.gitlab.com/fluidattacks/serves/exams:${CI_COMMIT_REF_NAME}"
  local context='containers/exams'
  local dockerfile='containers/exams/Dockerfile'

      aws_login \
  &&  sops_env 'secrets-prod.yaml' 'default' \
        ANSIBLE_VAULT \
  &&  build_arg_1='ANSIBLE_VAULT' \
  &&  helper_docker_build_and_push \
        "${tag}" \
        "${context}" \
        "${dockerfile}" \
        "${build_arg_1}" "${!build_arg_1}"
}

function job_deploy_docker_image_vpn {
  local tag="registry.gitlab.com/fluidattacks/serves/vpn:${CI_COMMIT_REF_NAME}"
  local context='containers/vpn'
  local dockerfile='containers/vpn/Dockerfile'

      aws_login \
  &&  sops_env 'secrets-prod.yaml' 'default' \
        ANSIBLE_VAULT \
  &&  build_arg_1='ANSIBLE_VAULT' \
  &&  helper_docker_build_and_push \
        "${tag}" \
        "${context}" \
        "${dockerfile}" \
        "${build_arg_1}" "${!build_arg_1}"
}

function _job_deploy_integrates {
  local bucket="fluidattacks-terraform-states-prod"
  local b64_aws_access_key_id
  local b64_aws_secret_access_key
  local output_key_id_name='integrates-prod-secret-key-id'
  local output_secret_key_name='integrates-prod-secret-key'
  local temp_aws_access_key_id
  local temp_aws_secret_access_key
  local terraform_dir="services/user-provision-integrates/integrates-prod/terraform"

      echo '[INFO] Deploying Integrates app: adding date' \
  &&  sed -i "s/\$date/$(date)/g" \
        infrastructure/eks/manifests/deployments/*.yaml \
  &&  echo '[INFO] Deploying Integrates app: computing AWS keys' \
  &&  temp_aws_access_key_id=$( \
        helper_terraform_output \
          "${terraform_dir}" \
          "${bucket}" \
          "${output_key_id_name}") \
  &&  temp_aws_secret_access_key=$( \
        helper_terraform_output \
          "${terraform_dir}" \
          "${bucket}" \
          "${output_key_id_name}") \
  &&  b64_aws_access_key_id=$( \
        echo -n "${temp_aws_access_key_id}" | base64) \
  &&  b64_aws_secret_access_key=$( \
        echo -n "${temp_aws_secret_access_key}" | base64) \
  &&  echo '[INFO] Deploying Integrates app: adding AWS keys to manifest' \
  &&  sed -i "s/\$b64_aws_access_key_id/${b64_aws_access_key_id}/g" \
        infrastructure/eks/manifests/deployments/integrates-app.yaml \
  &&  sed -i "s/\$b64_aws_secret_access_key/${b64_aws_secret_access_key}/g" \
        infrastructure/eks/manifests/deployments/integrates-app.yaml \
  &&  echo '[INFO] Deploying Integrates app: configuring kubeconfig and namespace' \
  &&  aws eks update-kubeconfig --name 'FluidServes' --region 'us-east-1' \
  &&  kubectl config \
        set-context "$(kubectl config current-context)" \
        --namespace serves \
  &&  echo '[INFO] Deploying Integrates app: kubectl apply' \
  &&  kubectl apply \
        -f infrastructure/eks/manifests/deployments/integrates-app.yaml \
  &&  if kubectl rollout status deploy/integrates-app --timeout=10m
      then
            echo '[INFO] Deploying Integrates app: success' \
        &&  return 0
      else
            echo '[ERROR] Deploying Integrates app: kubectl rollout failed' \
        &&  echo '[INFO] Deploying Integrates app: undoing deploy' \
        &&  kubectl rollout undo deploy/integrates-app  \
        &&  return 1
      fi
}

function job_run_break_build_dynamic {
  helper_run_break_build 'dynamic'
}

function job_run_break_build_static {
  helper_run_break_build 'static'
}

function job_lint_code {
  local path
  local path_basename

  # SC1090: Can't follow non-constant source. Use a directive to specify location.
  # SC2016: Expressions don't expand in single quotes, use double quotes for that.
  # SC2154: var is referenced but not assigned.

      nix-linter --recursive . \
  && echo '[OK] Nix code is compliant'
      shellcheck --external-sources build.sh \
  && find '.' -name '*.sh' -exec \
      shellcheck --external-sources --exclude=SC1090,SC2016,SC2154 {} + \
  && echo '[OK] Shell code is compliant' \
  && find . -type f -name '*.py' \
      | (grep -vP './analytics/singer' || cat) \
      | while read -r path
        do
          echo "[INFO] linting python file: ${path}" \
          && mypy \
                --ignore-missing-imports \
                --no-incremental \
              "${path}" \
          || return 1
        done \
  && pushd analytics/singer \
    && find "${PWD}" -mindepth 1 -maxdepth 1 -type d \
      | while read -r path
        do
          echo "[INFO] linting python package: ${path}" \
          && path_basename=$(basename "${path}") \
          && mypy \
                --ignore-missing-imports \
                --no-incremental \
              "${path_basename}" \
          || return 1
        done \
  && popd \
  && prospector --profile .prospector.yml .
}

function job_infra_analytics_test {
      helper_terraform_init \
        services/analytics/terraform \
        fluidattacks-terraform-states-prod \
  &&  helper_terraform_plan \
        services/analytics/terraform \
        fluidattacks-terraform-states-prod
}

function job_infra_analytics_deploy {
      helper_terraform_apply \
        services/analytics/terraform \
        fluidattacks-terraform-states-prod
}

function job_infra_autoscaling_ci_test {
      helper_terraform_init \
        services/autoscaling-ci/terraform \
        fluidattacks-terraform-states-prod \
  &&  helper_terraform_plan \
        services/autoscaling-ci/terraform \
        fluidattacks-terraform-states-prod
}

function job_infra_autoscaling_ci_deploy {
      helper_terraform_apply \
        services/autoscaling-ci/terraform \
        fluidattacks-terraform-states-prod
}

function job_infra_aws_sso_test {
      helper_terraform_init \
        services/aws-sso/terraform \
        fluidattacks-terraform-states-prod \
  &&  helper_terraform_plan \
        services/aws-sso/terraform \
        fluidattacks-terraform-states-prod
}

function job_infra_aws_sso_deploy {
      helper_terraform_apply \
        services/aws-sso/terraform \
        fluidattacks-terraform-states-prod
}

function job_infra_eks_setup {
      echo '[INFO] This is a work in progress! this may fail' \
  &&  . services/eks-cluster/kubectl-setup/kubectl-setup.sh \
  &&  . services/eks-cluster/helm/installation/deploy-helm.sh \
  &&  kubectl_setup \
  &&  deploy_helm
}

function job_infra_eks_test {
      echo '[INFO] This is a work in progress! this may fail' \
  &&  helper_terraform_init \
        services/eks/terraform \
        fluidattacks-terraform-states-prod \
  &&  helper_terraform_plan \
        services/eks/terraform \
        fluidattacks-terraform-states-prod
}

function job_infra_eks_deploy {
      echo '[INFO] This is a work in progress! this may fail' \
  &&  helper_terraform_apply \
        services/eks/terraform \
        fluidattacks-terraform-states-prod
}

function job_infra_fluid_vpc_test {
      helper_terraform_init \
        services/fluid-vpc/terraform \
        fluidattacks-terraform-states-prod \
  &&  helper_terraform_plan \
        services/fluid-vpc/terraform \
        fluidattacks-terraform-states-prod
}

function job_infra_fluid_vpc_deploy {
      helper_terraform_apply \
        services/fluid-vpc/terraform \
        fluidattacks-terraform-states-prod
}

function _job_infra_monolith {
  export TF_VAR_elbDns
  export TF_VAR_elbZone
  export VAULT_KMS_KEY
  local elbs_info
  local elbs_names
  local helm_home
  local jq_query
  local name
  local tags
  local terraform_state
  local users_integrates
  local first_argument="${1}"

      aws_login \
  &&  aws eks update-kubeconfig \
        --name 'FluidServes' --region 'us-east-1' \
  &&  kubectl config \
        set-context "$(kubectl config current-context)" --namespace 'serves' \
  &&  sops_env secrets-prod.yaml default \
        AUTONOMIC_TLS_CERT \
        AUTONOMIC_TLS_KEY \
        FA_RUNNER_TOKEN \
        FLUIDATTACKS_TLS_CERT \
        FLUID_TLS_KEY \
        FS_RUNNER_TOKEN \
        HELM_CA \
        HELM_CERT \
        HELM_KEY \
        NRIA_LICENSE_KEY \
        ONELOGIN_FINANCE_SSO \
        ONELOGIN_SSO \
        TF_VAR_dbName \
        TF_VAR_dbPass \
        TF_VAR_dbSnapId \
        TF_VAR_dbUser \
        TF_VAR_engineVersion \
        TILLER_CERT \
        TILLER_KEY \
  &&  pushd infrastructure/ \
    &&  echo "${ONELOGIN_SSO}" | base64 -d > SSO.xml \
    &&  echo "${ONELOGIN_FINANCE_SSO}" | base64 -d > SSOFinance.xml \
    &&  terraform init --backend-config="bucket=servestf" \
    &&  tflint \
    &&  terraform_state=$(mktemp) \
    &&  terraform plan \
          -out="${terraform_state}" \
          -refresh=true \
    &&  if [ "${first_argument}" == "deploy" ]; then
              terraform apply "${terraform_state}" \
          &&  helm_home="$(helm home)" \
          &&  mkdir -p "${helm_home}" \
          &&  base64 -d > "${helm_home}/key.pem"  <<< "${HELM_KEY}" \
          &&  base64 -d > "${helm_home}/cert.pem" <<< "${HELM_CERT}" \
          &&  base64 -d > "${helm_home}/ca.pem"   <<< "${HELM_CA}" \
          &&  VAULT_KMS_KEY=$(terraform output vaultKmsKey) \
          &&  eks/manifests/deploy.sh
        fi \
    &&  {
          users_integrates=$( \
            aws iam list-users \
              | jq '.Users[].Arn' \
                | grep -E 'integrates-prod' \
                  | head -n 1)
          echo "fiS3Arn = ${users_integrates}"
          terraform output 'dbEndpoint'
          terraform output 'fwBucket'
          terraform output 'fiBucket'
        } >> dns/terraform.tfvars \
    &&  pushd dns/ \
      &&  elbs_info="$(mktemp)" \
      &&  jq_query='.TagDescriptions[0].Tags[] | select(.Key == "kubernetes.io/cluster/FluidServes")' \
      &&  aws elb --region 'us-east-1' describe-load-balancers \
            > "${elbs_info}" \
      &&  elbs_names=$( \
            jq -r '.LoadBalancerDescriptions[].LoadBalancerName' "${elbs_info}") \
      &&  for name in ${elbs_names}; do
                tags="$(mktemp)" \
            &&  aws elb --region 'us-east-1' describe-tags \
                  --load-balancer-names "${name}" > "${tags}" \
            &&  if jq -e "${jq_query}" "${tags}"; then
                      TF_VAR_elbDns=$( \
                        jq -r ".LoadBalancerDescriptions[] \
                          | select(.LoadBalancerName == \"${name}\") \
                            | .DNSName" "${elbs_info}") \
                  &&  TF_VAR_elbZone=$( \
                        jq -r ".LoadBalancerDescriptions[] \
                          | select(.LoadBalancerName == \"${name}\") \
                            | .CanonicalHostedZoneNameID" "${elbs_info}")
                fi
          done || (
            echo "[ERROR] No nginx production load balancer was found"
            return 1
          ) \
      &&  terraform init --backend-config="bucket=servestf" \
      &&  tflint \
      &&  terraform plan \
          -out="${terraform_state}" \
          -refresh=true \
      &&  if [ "${first_argument}" == "deploy" ]; then
                terraform apply -auto-approve "${terraform_state}"
          fi \
   &&  popd \
  &&  popd \
  || return 1
}

function job_infra_monolith_test {
  _job_infra_monolith 'test'
}

function job_infra_monolith_deploy {
  _job_infra_monolith 'deploy'
}

function job_infra_sops_test {
      helper_terraform_init \
        services/sops/terraform \
        fluidattacks-terraform-states-prod \
  &&  helper_terraform_plan \
        services/sops/terraform \
        fluidattacks-terraform-states-prod
}

function job_infra_sops_deploy {
      helper_terraform_apply \
        services/sops/terraform \
        fluidattacks-terraform-states-prod
}

function job_send_new_version_email {
  local source_file

      source_file=$(mktemp) \
  &&  echo '[INFO] Logging in to aws' \
  &&  aws_login \
  &&  echo '[INFO] Exporting secrets' \
  &&  sops_env secrets-prod.yaml default \
        MANDRILL_APIKEY \
        MANDRILL_EMAIL_TO \
  &&  echo '[INFO] Generating script to send the email' \
  &&  cp "${srcExternalMail}" "${source_file}" \
  &&  echo "send_mail(
        'new_version',
        MANDRILL_EMAIL_TO,
        context={
          'project': PROJECT,
          'project_url': '${CI_PROJECT_URL}',
          'version': _get_version_date(),
          'message': _get_message(),
        },
        tags=[
          'general'
        ])" >> "${source_file}" \
  &&  cat "${source_file}" \
  &&  echo '[INFO] Executing' \
  &&  python "${source_file}"
}

function job_user_provision_continuous_dev_test {
      helper_terraform_init \
        services/user-provision-continuous/continuous-dev/terraform \
        fluidattacks-terraform-states-dev \
  &&  helper_terraform_plan \
        services/user-provision-continuous/continuous-dev/terraform \
        fluidattacks-terraform-states-dev
}

function job_user_provision_continuous_dev_deploy {
      helper_terraform_apply \
        services/user-provision-continuous/continuous-dev/terraform \
        fluidattacks-terraform-states-dev
}

function job_user_provision_continuous_dev_rotate_keys {
  local terraform_dir='services/user-provision-continuous/continuous-dev/terraform'
  local bucket='fluidattacks-terraform-states-dev'
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
        "${bucket}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}"
}

function job_user_provision_continuous_prod_test {
      helper_terraform_init \
        services/user-provision-continuous/continuous-prod/terraform \
        fluidattacks-terraform-states-prod \
  &&  helper_terraform_plan \
        services/user-provision-continuous/continuous-prod/terraform \
        fluidattacks-terraform-states-prod
}

function job_user_provision_continuous_prod_deploy {
      helper_terraform_apply \
        services/user-provision-continuous/continuous-prod/terraform \
        fluidattacks-terraform-states-prod
}

function job_user_provision_continuous_prod_rotate_keys {
  local terraform_dir='services/user-provision-continuous/continuous-prod/terraform'
  local bucket='fluidattacks-terraform-states-prod'
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
        "${bucket}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}"
}

function job_user_provision_integrates_dev_test {
      helper_terraform_init \
        services/user-provision-integrates/integrates-dev/terraform \
        fluidattacks-terraform-states-prod \
  &&  helper_terraform_plan \
        services/user-provision-integrates/integrates-dev/terraform \
        fluidattacks-terraform-states-prod
}

function job_user_provision_integrates_dev_deploy {
      helper_terraform_apply \
        services/user-provision-integrates/integrates-dev/terraform \
        fluidattacks-terraform-states-prod
}

function job_user_provision_integrates_dev_rotate_keys {
  local terraform_dir='services/user-provision-integrates/integrates-dev/terraform'
  local bucket='fluidattacks-terraform-states-prod'
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
        "${bucket}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}"
}

function job_user_provision_integrates_prod_test {
      helper_terraform_init \
        services/user-provision-integrates/integrates-prod/terraform \
        fluidattacks-terraform-states-prod \
  &&  helper_terraform_plan \
        services/user-provision-integrates/integrates-prod/terraform \
        fluidattacks-terraform-states-prod
}

function job_user_provision_integrates_prod_deploy {
      helper_terraform_apply \
        services/user-provision-integrates/integrates-prod/terraform \
        fluidattacks-terraform-states-prod
}

function job_user_provision_integrates_prod_rotate_keys {
  local terraform_dir='services/user-provision-integrates/integrates-prod/terraform'
  local bucket='fluidattacks-terraform-states-prod'
  local resource_to_taint='aws_iam_access_key.integrates-prod-key'
  local output_key_id_name='integrates-prod-secret-key-id'
  local output_secret_key_name='integrates-prod-secret-key'
  local gitlab_repo_id='4620828'
  local gitlab_key_id_name='PROD_AWS_ACCESS_KEY_ID'
  local gitlab_secret_key_name='PROD_AWS_SECRET_ACCESS_KEY'
  local gitlab_masked='true'
  local gitlab_protected='true'

      helper_user_provision_rotate_keys \
        "${terraform_dir}" \
        "${bucket}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}" \
  &&  _job_deploy_integrates
}

function job_user_provision_web_prod_test {
      helper_terraform_init \
        services/user-provision-web/web-prod/terraform \
        fluidattacks-terraform-states-prod \
  &&  helper_terraform_plan \
        services/user-provision-web/web-prod/terraform \
        fluidattacks-terraform-states-prod
}

function job_user_provision_web_prod_deploy {
      helper_terraform_apply \
        services/user-provision-web/web-prod/terraform \
        fluidattacks-terraform-states-prod
}

function job_user_provision_web_prod_rotate_keys {
  local terraform_dir='services/user-provision-web/web-prod/terraform'
  local bucket='fluidattacks-terraform-states-prod'
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
        "${bucket}" \
        "${resource_to_taint}" \
        "${output_key_id_name}" \
        "${output_secret_key_name}" \
        "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" \
        "${gitlab_secret_key_name}" \
        "${gitlab_masked}" \
        "${gitlab_protected}"
}
