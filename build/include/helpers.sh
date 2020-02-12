# shellcheck shell=bash

function helper_indent_2 {
  sed 's/^/  /g'
}

function helper_list_declared_jobs {
  declare -F | sed 's/declare -f //' | grep -P '^job_[a-z_]+' | sed 's/job_//' | sort
}

function helper_list_vars_with_regex {
  local regex="${1}"
  printenv | grep -oP "${regex}" | sort
}

function helper_list_touched_files_in_last_commit {
  local path

  git show --format= --name-only HEAD \
    | while read -r path
      do
        if test -e "${path}"
        then
          echo "${path}"
        fi
      done
}

function helper_run_break_build {
  local kind="${1}"

      docker pull fluidattacks/break-build \
  &&  if test "${IS_LOCAL_BUILD}"
      then
        docker run fluidattacks/break-build \
            "--${kind}" \
            --id "${BREAK_BUILD_ID}" \
            --secret "${BREAK_BUILD_SECRET}" \
            --no-image-rm \
          | bash
      else
        docker run fluidattacks/break-build \
            "--${kind}" \
            --id "${BREAK_BUILD_ID}" \
            --secret "${BREAK_BUILD_SECRET}" \
            --no-image-rm \
            --gitlab-docker-socket-binding \
          | bash
      fi
}

function helper_terraform_apply {
  local target_dir="${1}"
  local bucket="${2}"

      helper_terraform_init "${target_dir}" "${bucket}" \
  &&  pushd "${target_dir}" \
    &&  echo '[INFO] Running terraform apply' \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd
}

function helper_terraform_init {
  local target_dir="${1}"
  local bucket="${2}"

      source toolbox/others.sh \
  &&  echo '[INFO] Logging in to aws' \
  &&  aws_login \
  &&  pushd "${target_dir}" \
    &&  echo '[INFO] Running terraform init' \
    &&  terraform init --backend-config="bucket=${bucket}" \
  &&  popd
}

function helper_terraform_lint {
  local target_dir="${1}"
  local bucket="${2}"

      helper_terraform_init "${target_dir}" "${bucket}" \
  &&  pushd "${1}" \
    &&  echo '[INFO] Running terraform linter' \
    &&  tflint --deep --module \
  &&  popd
}

function helper_terraform_plan {
  local target_dir="${1}"
  local bucket="${2}"

      helper_terraform_init "${target_dir}" "${bucket}" \
  &&  pushd "${target_dir}" \
    &&  echo '[INFO] Running terraform plan' \
    &&  terraform plan -refresh=true \
  &&  popd
}

function helper_terraform_taint {
  local target_dir="${1}"
  local bucket="${2}"
  local marked_value="${3}"

      helper_terraform_init "${target_dir}" "${bucket}" \
  &&  pushd "${target_dir}" \
    &&  terraform refresh \
    &&  echo "[INFO] Running terraform taint: ${marked_value}" \
    &&  terraform taint "${marked_value}" \
  &&  popd
}

function helper_terraform_output {
  local target_dir="${1}"
  local bucket="${2}"
  local output_name="${3}"

      helper_terraform_init "${target_dir}" "${bucket}" \
  &&  pushd "${target_dir}" \
    &&  echo "[INFO] Running terraform output: ${output_name}" \
    &&  terraform output "${output_name}" \
  &&  popd
}
