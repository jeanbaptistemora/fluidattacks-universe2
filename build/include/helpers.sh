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
