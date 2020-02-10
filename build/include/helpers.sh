# shellcheck shell=bash

function helper_indent_2 {
  sed 's/^/  /g'
}

function helper_list_declared_jobs {
  declare -F | grep -oP 'job_[a-z_]+' | sort
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
