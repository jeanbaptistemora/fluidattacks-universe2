# shellcheck shell=bash

source "${srcIncludeHelpers}"
source "${srcExternalSops}"
source "${srcDotDotToolboxOthers}"

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
