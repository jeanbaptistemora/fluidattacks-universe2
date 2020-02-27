# shellcheck shell=bash

source "${srcIncludeHelpers}"
source "${srcExternalGitlabVariables}"
source "${srcExternalSops}"
source "${srcDotDotToolboxOthers}"

function job_analytics_continuous_toe {
      aws_login \
  &&  sops_env secrets-prod.yaml default \
        analytics_gitlab_user \
        analytics_gitlab_token \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  pushd analytics/continuous \
    &&  echo '[INFO] Cloning continuous repository' \
    &&  git clone --depth 1 --single-branch \
          "https://${analytics_gitlab_user}:${analytics_gitlab_token}@gitlab.com/fluidattacks/continuous.git" \
    &&  echo '[INFO] Running streamer' \
    &&  ./streamer_toe.py \
          > .jsonstream \
    &&  echo '[INFO] Running tap' \
    &&  tap-json  \
          > .singer \
          < .jsonstream \
    &&  echo '[INFO] Running target' \
    &&  target-redshift \
          --auth "${TEMP_FILE2}" \
          --drop-schema \
          --schema-name 'continuous_toe' \
          < .singer \
  && popd
}

function job_analytics_dynamodb {
      aws_login \
  &&  sops_env secrets-prod.yaml default \
        analytics_aws_access_key \
        analytics_aws_secret_key \
        analytics_aws_default_region \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  {
        echo '{'
        echo "\"AWS_ACCESS_KEY_ID\":\"${analytics_aws_access_key}\","
        echo "\"AWS_SECRET_ACCESS_KEY\":\"${analytics_aws_secret_key}\","
        echo "\"AWS_DEFAULT_REGION\":\"${analytics_aws_default_region}\""
        echo '}'
      } > "${TEMP_FILE1}" \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  echo '[INFO] Running tap' \
  &&  mkdir ./logs \
  &&  tap-awsdynamodb \
        --auth "${TEMP_FILE1}" \
        --conf ./analytics/conf/awsdynamodb.json \
        > .singer \
  &&  echo '[INFO] Running target' \
  &&  target-redshift \
        --auth "${TEMP_FILE2}" \
        --drop-schema \
        --schema-name 'dynamodb' \
        < .singer
}

function job_analytics_formstack {
      aws_login \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_redshift \
        analytics_auth_formstack \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_formstack}" > "${TEMP_FILE1}" \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  echo '[INFO] Running tap' \
  &&  mkdir ./logs \
  &&  tap-formstack \
        --auth "${TEMP_FILE1}" \
        --conf ./analytics/conf/formstack.json \
        > .singer \
  &&  echo '[INFO] Running target' \
  &&  target-redshift \
        --auth "${TEMP_FILE2}" \
        --drop-schema \
        --schema-name 'formstack' \
        < .singer
}

function job_analytics_git {
  local fork
  local log_file
  local num_threads='8'
  local mock_integrates_api_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.xxx'

      aws_login \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_redshift \
        analytics_gitlab_user \
        analytics_gitlab_token \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  log_file=$(mktemp) \
  &&  echo '[INFO] Cloning our own repositories' \
  &&  python3 analytics/git/clone_us.py \
        | tee "${log_file}" \
  &&  echo '[INFO] Cloning our own repositories: uploading log' \
  &&  aws s3 cp "${log_file}" s3://fluidanalytics/clone_us.log \
  &&  echo '[INFO] Cloning customer repositories' \
  &&  \
      CI=true \
      DEV_AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
      DEV_AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
      INTEGRATES_API_TOKEN="${mock_integrates_api_token}" \
      PROD_AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
      PROD_AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
      python3 analytics/git/clone_them.py  \
        | tee "${log_file}" \
  &&  echo '[INFO] Cloning customer repositories: uploading log' \
  &&  aws s3 cp "${log_file}" s3://fluidanalytics/clone_them.log \
  &&  echo '[INFO] Generating stats' \
  &&  python3 analytics/git/generate_stats.py \
        || true \
  &&  echo '[INFO] Generating config' \
  &&  python3 analytics/git/generate_config.py 2>&1 \
        | aws s3 cp - s3://fluidanalytics/generate_config.log \
  &&  echo "[INFO] Running tap in ${num_threads} threads" \
  &&  for fork in $(seq 1 "${num_threads}")
      do
        ( tap-git \
            --conf './config.json' \
            --with-metrics \
            --threads "${num_threads}" \
            --fork-id "${fork}" > "git_part${fork}" ) &
      done \
  &&  wait \
  &&  echo '[INFO] Running target' \
  &&  cat git_part* \
        | target-redshift \
            --auth "${TEMP_FILE2}" \
            --drop-schema \
            --schema-name "git" \
  &&  echo '[INFO] Tainting ToEs' \
  &&  ./analytics/git/taint_all.sh
}

function job_analytics_infrastructure {
      aws_login \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_infra \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_infra}" > "${TEMP_FILE1}" \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  echo '[INFO] Running streamer' \
  &&  streamer-infrastructure \
        --auth "${TEMP_FILE1}" \
        > .jsonstream \
  &&  echo '[INFO] Running tap' \
  &&  tap-json \
        > .singer \
        < .jsonstream \
  &&  echo '[INFO] Running target' \
  &&  target-redshift \
        --auth "${TEMP_FILE2}" \
        --drop-schema \
        --schema-name 'infrastructure' \
        < .singer
}

function job_analytics_intercom {
      aws_login \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_intercom \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_intercom}" > "${TEMP_FILE1}" \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  echo '[INFO] Running streamer' \
  &&  streamer-intercom \
        --auth "${TEMP_FILE1}" \
        > .jsonstream \
  &&  echo '[INFO] Running tap' \
  &&  tap-json \
        --enable-timestamps \
        > .singer \
        < .jsonstream \
  &&  echo '[INFO] Running target' \
  &&  target-redshift \
        --auth "${TEMP_FILE2}" \
        --drop-schema \
        --schema-name 'intercom' \
        < .singer
}

function job_analytics_mandrill {
      aws_login \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_mandrill \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_mandrill}" > "${TEMP_FILE1}" \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  echo '[INFO] Running streamer' \
  &&  streamer-mandrill \
        --auth "${TEMP_FILE1}" \
        > .jsonstream \
  &&  echo '[INFO] Running tap' \
  &&  tap-json  \
        --date-formats '%Y-%m-%d %H:%M:%S,%Y-%m-%d %H:%M:%S.%f' \
        > .singer \
        < .jsonstream \
  &&  echo '[INFO] Running target' \
  &&  target-redshift \
        --auth "${TEMP_FILE2}" \
        --drop-schema \
        --schema-name 'mandrill' \
        < .singer
}

function job_analytics_gitlab {
  export GITLAB_PASS
  local project
  local projects=(
    'autonomicmind/default'
    'autonomicmind/training'
    'fluidattacks/continuous'
    'fluidattacks/asserts'
    'fluidattacks/integrates'
    'fluidattacks/private'
    'fluidattacks/public'
    'fluidattacks/serves'
    'fluidattacks/web'
    'fluidattacks/writeups'
  )

      aws_login \
  &&  sops_env secrets-prod.yaml default \
        analytics_gitlab_token \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  echo '[INFO] Running streamer' \
  &&  for project in "${projects[@]}"
      do
        GITLAB_PASS="${analytics_gitlab_token}" \
        ./analytics/singer/streamer_gitlab.py "${project}" >> .jsonstream \
            || return 1
      done \
  &&  echo '[INFO] Running tap' \
  &&  tap-json  \
        > .singer \
        < .jsonstream \
  &&  echo '[INFO] Running target' \
  &&  target-redshift \
        --auth "${TEMP_FILE2}" \
        --drop-schema \
        --schema-name 'gitlab-ci' \
        < .singer
}

function job_analytics_timedoctor_manually_create_token {
      aws_login \
  &&  sops_env secrets-prod.yaml default \
        analytics_auth_timedoctor \
        analytics_gitlab_token \
  &&  echo '[INFO] Executing creator, follow the steps' \
  &&  ./analytics/auth_helper.py --timedoctor-start \
  &&  echo '[INFO] Done! Token created at GitLab/serves env vars'
}

function job_analytics_timedoctor_refresh_token {
  export analytics_auth_timedoctor

      aws_login \
  &&  sops_env secrets-prod.yaml default \
        analytics_gitlab_token \
  &&  analytics_auth_timedoctor=$( \
        helper_get_gitlab_var \
          'analytics_auth_timedoctor' \
          "${analytics_gitlab_token}") \
  &&  echo '[INFO] Updating token...' \
  &&  ./analytics/auth_helper.py --timedoctor-refresh \
  &&  echo '[INFO] Done! Token created at GitLab/serves env vars'
}

function job_analytics_timedoctor {
  export analytics_auth_timedoctor

      aws_login \
  &&  mkdir ./logs \
  &&  sops_env secrets-prod.yaml default \
        analytics_aws_access_key \
        analytics_aws_secret_key \
        analytics_aws_default_region \
        analytics_auth_redshift \
        analytics_gitlab_token \
        analytics_s3_cache_timedoctor \
  &&  analytics_auth_timedoctor=$( \
        helper_get_gitlab_var \
          'analytics_auth_timedoctor' \
          "${analytics_gitlab_token}") \
  &&  echo '[INFO] Generating secret files' \
  &&  {
        echo '{'
        echo "\"AWS_ACCESS_KEY_ID\":\"${analytics_aws_access_key}\","
        echo "\"AWS_SECRET_ACCESS_KEY\":\"${analytics_aws_secret_key}\","
        echo "\"AWS_DEFAULT_REGION\":\"${analytics_aws_default_region}\""
        echo '}'
      } > "${TEMP_FILE1}" \
  &&  echo "${analytics_s3_cache_timedoctor}" > ./s3_files.json \
  &&  echo "${analytics_auth_timedoctor}" > "${TEMP_FILE2}" \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE3}" \
  &&  echo '[INFO] Downloading backups from S3' \
  &&  python3 analytics/download_from_aws_sss.py \
        -auth "${TEMP_FILE1}" \
        -conf './s3_files.json' \
  &&  cat 'timedoctor.worklogs.2013-01-01.2018-12-31.singer' \
        > .singer \
  &&  cat 'timedoctor.computer_activity.2018-01-01.2018-12-31.singer' \
        >> .singer \
  &&  echo '[INFO] Running tap' \
  &&  tap-timedoctor \
        --auth "${TEMP_FILE2}" \
        >> .singer \
  &&  echo '[INFO] Running target' \
  &&  target-redshift \
        --auth "${TEMP_FILE3}" \
        --drop-schema \
        --schema-name 'timedoctor' \
        < .singer
}

function job_analytics_zoho {
  local analytics_zoho_tables=(
    Candidates
    Periods
  )

      aws_login \
  &&  sops_env secrets-prod.yaml default \
        analytics_zoho_email \
        analytics_zoho_token \
        analytics_zoho_space \
        analytics_auth_redshift \
  &&  echo '[INFO] Generating secret files' \
  &&  echo "${analytics_auth_redshift}" > "${TEMP_FILE2}" \
  &&  echo '[INFO] Running converter and streamer' \
  &&  for table in "${analytics_zoho_tables[@]}"
      do
            echo "  [INFO] Table: ${table}" \
        &&  ./analytics/singer/converter_zoho_csv.py \
              --email "${analytics_zoho_email}" \
              --token "${analytics_zoho_token}" \
              --space "${analytics_zoho_space}" \
              --table "${table}" \
              --target "${table}" \
        &&  ./analytics/singer/streamer_csv.py "${table}" \
              >> .jsonstream \
        || return 1
      done \
  &&  echo '[INFO] Running tap' \
  &&  tap-json  \
        --date-formats '%Y-%m-%d %H:%M:%S' \
        > .singer \
        < .jsonstream \
  &&  echo '[INFO] Running target' \
  &&  target-redshift \
        --auth "${TEMP_FILE2}" \
        --drop-schema \
        --schema-name 'zoho' \
        < .singer
}

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

function job_deploy_docker_image_nix {
  local tag="${CI_REGISTRY_IMAGE}:nix"
  local context='.'
  local dockerfile='build/Dockerfile'

  helper_docker_build_and_push \
    "${tag}" \
    "${context}" \
    "${dockerfile}"
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
  # SC2153: Possible misspelling: TEMP_FILE2 may not be assigned, but TEMP_FILE1 is.
  # SC2154: var is referenced but not assigned.

      nix-linter --recursive . \
  && echo '[OK] Nix code is compliant'
      shellcheck --external-sources build.sh \
  && find '.' -name '*.sh' -exec \
      shellcheck --external-sources --exclude=SC1090,SC2016,SC2153,SC2154 {} + \
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
  &&  helper_terraform_plan \
        services/analytics/terraform
}

function job_infra_analytics_deploy {
      helper_terraform_apply \
        services/analytics/terraform
}

function job_infra_autoscaling_ci_test {
      helper_terraform_init \
        services/autoscaling-ci/terraform \
  &&  helper_terraform_plan \
        services/autoscaling-ci/terraform
}

function job_infra_autoscaling_ci_deploy {
      helper_terraform_apply \
        services/autoscaling-ci/terraform
}

function job_infra_autoscaling_ci_deploy_config {
  local bastion_ip='192.168.3.11'
  local bastion_user='ubuntu'
  local secrets_to_replace=(
    autoscaling_token_1
    autoscaling_token_2
    autoscaling_token_3
    autoscaling_access_key
    autoscaling_secret_key
  )

      echo '[INFO] Adding bastion to known hosts' \
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
        'sudo killall -SIGHUP gitlab-runner'
}

function job_infra_aws_sso_test {
      helper_terraform_init \
        services/aws-sso/terraform \
  &&  helper_terraform_plan \
        services/aws-sso/terraform
}

function job_infra_aws_sso_deploy {
      helper_terraform_apply \
        services/aws-sso/terraform
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
  &&  helper_terraform_plan \
        services/eks/terraform
}

function job_infra_eks_deploy {
      echo '[INFO] This is a work in progress! this may fail' \
  &&  helper_terraform_apply \
        services/eks/terraform
}

function job_infra_fluid_vpc_test {
      helper_terraform_init \
        services/fluid-vpc/terraform \
  &&  helper_terraform_plan \
        services/fluid-vpc/terraform
}

function job_infra_fluid_vpc_deploy {
      helper_terraform_apply \
        services/fluid-vpc/terraform
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
    &&  terraform init \
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
        } >> dns/terraform.tfvars \
    &&  pushd dns/ \
      &&  elbs_info="$(mktemp)" \
      &&  jq_query='.TagDescriptions[0].Tags[] | select(.Key == "kubernetes.io/cluster/FluidServes")' \
      &&  aws elb --region 'us-east-1' describe-load-balancers \
            > "${elbs_info}" \
      &&  elbs_names=$( \
            jq -r '.LoadBalancerDescriptions[].LoadBalancerName' "${elbs_info}") \
      &&  {
            for name in ${elbs_names}; do
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
            )
          } \
      &&  terraform init \
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
  &&  helper_terraform_plan \
        services/sops/terraform
}

function job_infra_sops_deploy {
      helper_terraform_apply \
        services/sops/terraform
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
        services/user-provision/continuous/dev/terraform \
  &&  helper_terraform_plan \
        services/user-provision/continuous/dev/terraform
}

function job_user_provision_continuous_dev_deploy {
      helper_terraform_apply \
        services/user-provision/continuous/dev/terraform
}

function job_user_provision_continuous_dev_rotate_keys {
  local terraform_dir='services/user-provision/continuous/dev/terraform'
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

function job_user_provision_continuous_prod_test {
      helper_terraform_init \
        services/user-provision/continuous/prod/terraform \
  &&  helper_terraform_plan \
        services/user-provision/continuous/prod/terraform
}

function job_user_provision_continuous_prod_deploy {
      helper_terraform_apply \
        services/user-provision/continuous/prod/terraform
}

function job_user_provision_continuous_prod_rotate_keys {
  local terraform_dir='services/user-provision/continuous/prod/terraform'
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

function job_user_provision_integrates_dev_test {
      helper_terraform_init \
        services/user-provision/integrates/dev/terraform \
  &&  helper_terraform_plan \
        services/user-provision/integrates/dev/terraform
}

function job_user_provision_integrates_dev_deploy {
      helper_terraform_apply \
        services/user-provision/integrates/dev/terraform
}

function job_user_provision_integrates_dev_rotate_keys {
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

function job_user_provision_integrates_prod_test {
      helper_terraform_init \
        services/user-provision/integrates/prod/terraform \
  &&  helper_terraform_plan \
        services/user-provision/integrates/prod/terraform
}

function job_user_provision_integrates_prod_deploy {
      helper_terraform_apply \
        services/user-provision/integrates/prod/terraform
}

function job_user_provision_integrates_prod_rotate_keys {
  local terraform_dir='services/user-provision/integrates/prod/terraform'
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

function job_user_provision_web_dev_test {
      helper_terraform_init \
        services/user-provision/web/dev/terraform \
  &&  helper_terraform_plan \
        services/user-provision/web/dev/terraform
}

function job_user_provision_web_dev_deploy {
      helper_terraform_apply \
        services/user-provision/web/dev/terraform
}

function job_user_provision_web_dev_rotate_keys {
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

function job_user_provision_web_prod_test {
      helper_terraform_init \
        services/user-provision/web/prod/terraform \
  &&  helper_terraform_plan \
        services/user-provision/web/prod/terraform
}

function job_user_provision_web_prod_deploy {
      helper_terraform_apply \
        services/user-provision/web/prod/terraform
}

function job_user_provision_web_prod_rotate_keys {
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

function _job_terraform_states_bucket {
  export TF_VAR_aws_access_key="${AWS_ACCESS_KEY_ID}"
  export TF_VAR_aws_secret_key="${AWS_SECRET_ACCESS_KEY}"
  local bucket="${1}"
  local sse_config

  if aws s3api list-buckets --query 'Buckets[].Name' | grep -q "${bucket}"
  then
        echo "[INFO] Bucket already exists: ${bucket}"
  else
        echo "[INFO] Creating bucket: ${bucket}" \
    &&  sse_config='{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}' \
    &&  aws s3api create-bucket \
          --bucket "${bucket}" \
          --region 'us-east-1' \
          --acl 'private' \
    &&  echo '[INFO] Activating versioning' \
    &&  aws s3api put-bucket-versioning \
          --bucket "${bucket}" \
          --versioning-configuration Status=Enabled \
    &&  echo '[INFO] Activating server side encryption' \
        aws s3api put-bucket-encryption \
          --bucket "$1" \
          --server-side-encryption-configuration "$sse_config"
  fi
}

function job_terraform_states_bucket {
      _job_terraform_states_bucket 'fluidattacks-terraform-states-prod' \
  &&  _job_terraform_states_bucket 'fluidattacks-terraform-states-dev'
}
