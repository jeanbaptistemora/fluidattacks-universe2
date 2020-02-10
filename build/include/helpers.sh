# shellcheck shell=bash

function helper_indent_2 {
  sed 's/^/  /g'
}

function helper_list_declared_jobs {
  declare -F | grep -oP 'job_[a-z_]+' | sort
}
