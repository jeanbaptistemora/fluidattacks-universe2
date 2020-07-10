# shellcheck shell=bash

function helper_use_pristine_workdir {
  export WORKDIR
  export STARTDIR

  function helper_teardown_workdir {
        echo "[INFO] Deleting: ${WORKDIR}" \
    &&  rm -rf "${WORKDIR}"
  }
  trap 'helper_teardown_workdir' 'EXIT'

      echo '[INFO] Creating a pristine workdir' \
  &&  rm -rf "${WORKDIR}" \
  &&  mkdir -p "${WORKDIR}" \
  &&  echo '[INFO] Copying files to workdir' \
  &&  cp -r "${STARTDIR}/." "${WORKDIR}" \
  &&  echo '[INFO] Entering the workdir' \
  &&  pushd "${WORKDIR}" \
  &&  echo '[INFO] Running: git clean -xdf' \
  &&  git clean -xdf \
  ||  return 1
}

function helper_docker_build_and_push {
  local tag="${1}"
  local context="${2}"
  local dockerfile="${3}"
  local build_arg_1_key="${4:-build_arg_1_key}"
  local build_arg_1_val="${5:-build_arg_1_val}"
  local build_arg_2_key="${6:-build_arg_2_key}"
  local build_arg_2_val="${7:-build_arg_2_val}"
  local build_arg_3_key="${8:-build_arg_3_key}"
  local build_arg_3_val="${9:-build_arg_3_val}"
  local build_arg_4_key="${10:-build_arg_4_key}"
  local build_arg_4_val="${11:-build_arg_4_val}"
  local build_arg_5_key="${12:-build_arg_5_key}"
  local build_arg_5_val="${13:-build_arg_5_val}"
  local build_arg_6_key="${14:-build_arg_6_key}"
  local build_arg_6_val="${15:-build_arg_6_val}"
  local build_arg_7_key="${16:-build_arg_7_key}"
  local build_arg_7_val="${17:-build_arg_7_val}"
  local build_arg_8_key="${18:-build_arg_8_key}"
  local build_arg_8_val="${19:-build_arg_8_val}"
  local build_arg_9_key="${20:-build_arg_9_key}"
  local build_arg_9_val="${21:-build_arg_9_val}"
  local build_args=(
    --tag "${tag}"
    --file "${dockerfile}"
    --build-arg "${build_arg_1_key}=${build_arg_1_val}"
    --build-arg "${build_arg_2_key}=${build_arg_2_val}"
    --build-arg "${build_arg_3_key}=${build_arg_3_val}"
    --build-arg "${build_arg_4_key}=${build_arg_4_val}"
    --build-arg "${build_arg_5_key}=${build_arg_5_val}"
    --build-arg "${build_arg_6_key}=${build_arg_6_val}"
    --build-arg "${build_arg_7_key}=${build_arg_7_val}"
    --build-arg "${build_arg_8_key}=${build_arg_8_val}"
    --build-arg "${build_arg_9_key}=${build_arg_9_val}"
  )

      echo "[INFO] Logging into: ${CI_REGISTRY}" \
  &&  docker login \
        --username "${CI_REGISTRY_USER}" \
        --password "${CI_REGISTRY_PASSWORD}" \
      "${CI_REGISTRY}" \
  &&  echo "[INFO] Pulling: ${tag}" \
  &&  if docker pull "${tag}"
      then
        build_args+=( --cache-from "${tag}" )
      fi \
  &&  echo "[INFO] Building: ${tag}" \
  &&  docker build "${build_args[@]}" "${context}" \
  &&  echo "[INFO] Pushing: ${tag}" \
  &&  docker push "${tag}" \
  &&  echo "[INFO] Deleting local copy of: ${tag}" \
  &&  docker image remove "${tag}"
}

function helper_list_declared_jobs {
  declare -F \
    | sed 's/declare -f //' \
    | grep -P '^job_[a-z_]+' \
    | sed 's/job_//' \
    | sort
}

function helper_list_touched_files {
  local path

  git show --format= --name-only HEAD | while read -r path
  do
    if test -e "${path}"
    then
      echo "${path}"
    fi
  done
}

function helper_file_exists {
  local path="${1}"

      if [ -f "${path}" ]
      then
            return 0
      else
            echo "[ERROR] ${path} does not exist" \
        &&  return 1
      fi
}

function helper_get_gitlab_var {
  local gitlab_var_name="${1}"
  local gitlab_api_token="${2}"

      echo "[INFO] Retrieving var from GitLab: ${gitlab_var_name}" 1>&2 \
  &&  curl \
        --silent \
        --header "private-token: ${gitlab_api_token}" \
        "${GITLAB_API_URL}/${gitlab_var_name}" \
      | jq -r '.value'
}

function helper_move_artifacts_to_git {
  local artifacts="${PWD}/artifacts"
  local git="/git"

  if test -e "${artifacts}"
  then
    # shellcheck disable=SC2015
        echo '[INFO] Moving repositories from the artifacts to git' \
    &&  mv "${artifacts}/"* "${git}" \
    &&  ls "${git}" \
    ||  true
  fi
}

function helper_move_git_to_artifacts {
  local artifacts="${PWD}/artifacts"
  local git="/git"

      echo '[INFO] Moving repositories from git to artifacts' \
  &&  mkdir -p "${artifacts}" \
  &&  mv "${git}/"* "${artifacts}"
}

function helper_move_services_fusion_to_master_git {
  local mock_integrates_api_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.xxx'
  local path_empty_repos="${PWD}/repos_to_get_from_cache.lst"

  set +o errexit
  set +o nounset

  ls
  pushd '/git/fluidattacks/services'
    while read -r subs
    do
          echo "[INFO] Fetching ${subs} from S3" \
      &&  CI='true' \
          CI_COMMIT_REF_NAME='master' \
          INTEGRATES_API_TOKEN="${mock_integrates_api_token}" \
          PROD_AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
          PROD_AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
          fluid drills --pull-repos "${subs}" \
      &&  mkdir -p ../../"${subs}" \
      &&  cp -r groups/"${subs}"/fusion/* ../../"${subs}"
    done < "${path_empty_repos}"
  popd

  set -o errexit
  set -o nounset
}

function helper_build_nix_caches_parallel {
  local n_provisioners
  local n_provisioners_per_group
  local n_provisioners_remaining
  export lower_limit
  export upper_limit

      n_provisioners=$(find build2/provisioners/ -type f | wc -l) \
  &&  n_provisioners_per_group=$(( n_provisioners/CI_NODE_TOTAL )) \
  &&  n_provisioners_remaining=$(( n_provisioners%CI_NODE_TOTAL )) \
  &&  if [ "${n_provisioners_remaining}" -gt '0' ]
      then
        n_provisioners_per_group=$(( n_provisioners_per_group+=1 ))
      fi \
  &&  lower_limit=$(( (CI_NODE_INDEX-1)*n_provisioners_per_group )) \
  &&  upper_limit=$(( CI_NODE_INDEX*n_provisioners_per_group-1 )) \
  &&  upper_limit=$((
        upper_limit > n_provisioners-1 ? n_provisioners-1 : upper_limit
      ))
}

function helper_aws_login {
      echo '[INFO] Logging into AWS' \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}"
}

function helper_terraform_login {
  export TF_VAR_aws_access_key
  export TF_VAR_aws_secret_key

      helper_aws_login \
  &&  echo '[INFO] Logging into Terraform' \
  &&  TF_VAR_aws_access_key="${AWS_ACCESS_KEY_ID}" \
  &&  TF_VAR_aws_secret_key="${AWS_SECRET_ACCESS_KEY}"
}

function helper_terraform_init {
  local target_dir="${1}"

      helper_terraform_login \
  &&  pushd "${target_dir}" \
    &&  echo '[INFO] Running terraform init' \
    &&  terraform init \
  &&  popd \
  || return 1
}

function helper_terraform_plan {
  local target_dir="${1}"

      helper_terraform_init "${target_dir}" \
  &&  pushd "${target_dir}" \
    &&  echo '[INFO] Running terraform plan' \
    &&  terraform plan -refresh=true \
    &&  tflint --deep --module \
  &&  popd \
  || return 1
}

function helper_terraform_apply {
  local target_dir="${1}"

      helper_terraform_init "${target_dir}" \
  &&  pushd "${target_dir}" \
    &&  echo '[INFO] Running terraform apply' \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  || return 1
}

function helper_terraform_taint {
  local target_dir="${1}"
  local marked_value="${2}"

      helper_terraform_init "${target_dir}" \
  &&  pushd "${target_dir}" \
    &&  terraform refresh \
    &&  echo "[INFO] Running terraform taint: ${marked_value}" \
    &&  terraform taint "${marked_value}" \
  &&  popd \
  || return 1
}

function helper_terraform_output {
  local target_dir="${1}"
  local output_name="${2}"

      helper_terraform_init "${target_dir}" 1>&2 \
  &&  pushd "${target_dir}" 1>&2 \
    &&  echo "[INFO] Running terraform output: ${output_name}" 1>&2 \
    &&  terraform output "${output_name}" \
  &&  popd 1>&2 \
  || return 1
}

function helper_infra_monolith {
  export TF_VAR_elbDns
  export TF_VAR_elbZone
  export VAULT_KMS_KEY
  local elbs_info
  local elbs_names
  local helm_home
  local jq_query
  local name
  local tags
  local first_argument="${1}"

      helper_aws_login \
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
        TILLER_CERT \
        TILLER_KEY \
  &&  pushd infrastructure/ || return 1 \
    &&  echo "${ONELOGIN_SSO}" | base64 -d > SSO.xml \
    &&  echo "${ONELOGIN_FINANCE_SSO}" | base64 -d > SSOFinance.xml \
    &&  helper_terraform_plan . \
    &&  if [ "${first_argument}" == "deploy" ]; then
              helper_terraform_apply . \
          &&  helm_home="$(helm home)" \
          &&  mkdir -p "${helm_home}" \
          &&  base64 -d > "${helm_home}/key.pem"  <<< "${HELM_KEY}" \
          &&  base64 -d > "${helm_home}/cert.pem" <<< "${HELM_CERT}" \
          &&  base64 -d > "${helm_home}/ca.pem"   <<< "${HELM_CA}" \
          &&  eks/manifests/deploy.sh
        fi \
    &&  pushd dns/ || return 1 \
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
      &&  helper_terraform_plan . \
      &&  if [ "${first_argument}" == "deploy" ]; then
                helper_terraform_apply .
          fi \
   &&  popd || return 1 \
  &&  popd || return 1 \
  || return 1
}

function helper_get_resource_to_taint_number {

  # Made specifically for nightly rotations.
  # It prints 1 if day is even and 2 if day is odd.

  local date
  local timestamp
  local days

      date="$(date +%y-%m-%d)" \
  &&  timestamp="$(date +%s --date="${date}")" \
  &&  days=$((timestamp / 60 / 60 / 24)) \
  &&  if [ $((days % 2)) == '0' ]
      then
        echo "1"
      else
        echo "2"
      fi
}

function helper_check_last_job_succeeded {
  export GITLAB_API_TOKEN
  local gitlab_repo_id="${1}"
  local job_name="${2}"
  local job_status=''
  local job_url=''
  local page='0'
  local job_data=''

      echo '[INFO] Iterating GitLab jobs' \
  &&  for page in $(seq 0 100)
      do
            echo "[INFO] Checking page ${page} for job: ${job_name}" \
        &&  if job_data=$( \
                  curl \
                      --globoff \
                      --silent \
                      --header "private-token: ${GITLAB_API_TOKEN}" \
                      "https://gitlab.com/api/v4/projects/${gitlab_repo_id}/jobs?page=${page}" \
                    | jq -er ".[] | select(.name == \"${job_name}\")")
            then
                  job_url=$(echo "${job_data}" | jq -er '.web_url') \
              &&  echo "[INFO] Got the job: ${job_url}" \
              &&  break
            else
              continue
            fi
      done \
  &&  if test -z "${job_data}"
      then
            echo '[INFO] Job was not found, was it renamed?' \
        &&  return 1
      fi \
  &&  job_status=$(echo "${job_data}" | jq -er '.status') \
  &&  if test "${job_status}" = "success"
      then
            echo "[INFO] Job status is: ${job_status}, continuing" \
        &&  return 0
      else
            echo "[INFO] Job status is different that succeeded: ${job_status}, continuing" \
        &&  return 1
      fi
}

function helper_user_provision_rotate_keys {
  local terraform_dir="${1}"
  local resource_to_taint="${2}"
  local output_key_id_name="${3}"
  local output_key_id_value
  local output_secret_key_name="${4}"
  local output_secret_key_value
  local gitlab_repo_id="${5}"
  local gitlab_key_id_name="${6}"
  local gitlab_secret_key_name="${7}"
  local gitlab_masked="${8}"
  local gitlab_protected="${9}"
  local resource_to_taint_number

      resource_to_taint_number="$( \
        helper_get_resource_to_taint_number)" \
  &&  helper_terraform_taint \
        "${terraform_dir}" \
        "${resource_to_taint}-${resource_to_taint_number}" \
  &&  helper_terraform_apply \
        "${terraform_dir}" \
  &&  output_key_id_value=$( \
        helper_terraform_output \
          "${terraform_dir}" \
          "${output_key_id_name}-${resource_to_taint_number}") \
  &&  output_secret_key_value=$( \
        helper_terraform_output \
          "${terraform_dir}" \
          "${output_secret_key_name}-${resource_to_taint_number}")  \
  &&  set_project_variable \
        "${GITLAB_API_TOKEN}" "${gitlab_repo_id}" \
        "${gitlab_key_id_name}" "${output_key_id_value}" \
        "${gitlab_protected}" "${gitlab_masked}" \
  &&  set_project_variable \
        "${GITLAB_API_TOKEN}" "${gitlab_repo_id}" \
        "${gitlab_secret_key_name}" "${output_secret_key_value}" \
        "${gitlab_protected}" "${gitlab_masked}"
}

function helper_test_commit_msg_commitlint {
  local commit_diff
  local commit_hashes
  local parser_url='https://gitlab.com/fluidattacks/public/-/raw/master/commitlint-configs/others/parser-preset.js'
  local rules_url='https://gitlab.com/fluidattacks/public/-/raw/master/commitlint-configs/others/commitlint.config.js'

      helper_use_pristine_workdir \
  &&  curl -LOJ "${parser_url}" \
  &&  curl -LOJ "${rules_url}" \
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
            echo  '[INFO] Running Commitlint' \
        &&  git log -1 --pretty=%B "${commit_hash}" | commitlint \
        ||  return 1
      done
}

function helper_test_lint_code_nix {
  local path="${1}"

  nix-linter --recursive "${path}"
}

function helper_test_lint_code_shell {
  local path="${1}"

  find "${path}" -name '*.sh' -exec \
    shellcheck --external-sources --exclude=SC1090,SC2016,SC2153,SC2154 {} +
}

function helper_test_lint_code_python {
      find . -type f -name '*.py' \
        | (grep -vP './analytics/singer' || cat) \
        | while read -r path
          do
                echo "[INFO] linting python file: ${path}" \
            &&  mypy \
                  --ignore-missing-imports \
                  --no-incremental \
                  "${path}" \
            || return 1
          done \
  &&  pushd analytics/singer || return 1 \
  &&  find "${PWD}" -mindepth 1 -maxdepth 1 -type d \
        | while read -r path
          do
                echo "[INFO] linting python package: ${path}" \
            &&  path_basename=$(basename "${path}") \
            &&  mypy \
                  --ignore-missing-imports \
                  --no-incremental \
                  "${path_basename}" \
            || return 1
          done \
  &&  popd || return 1 \
  &&  prospector --profile .prospector.yml .
}

function helper_test_forces {
  local kind="${1}"
  local args

      args=(
        "--${kind}"
        '--id'  "${BREAK_BUILD_ID}"
        '--secret' "${BREAK_BUILD_SECRET}"
        '--no-image-rm'
      ) \
  &&  docker pull fluidattacks/break-build \
  &&  pushd "${STARTDIR}" || return 1 \
  &&  if ! test "${IS_LOCAL_BUILD}"
      then
        args+=('--gitlab-docker-socket-binding')
      fi \
  &&  docker run fluidattacks/break-build \
        "${args[@]}" \
        | bash \
  &&  popd || return 1
}
