# shellcheck shell=bash

source '__envUtilsBashLibPython__'


function setup_runtime {
  IFS=' ' read -r -a python_req_srcs <<< "__envPythonReqsSrcs__" \
  &&  IFS=' ' read -r -a python_req_envs <<< "__envPythonReqsEnvs__" \
  &&  for pkg in "${python_req_envs[@]}"
      do
            make_python_path '3.8' \
              "${pkg}" \
        ||  return 1
      done \
  &&  for pkg in "${python_req_srcs[@]}"
      do
            make_python_path_plain "$pkg" \
        ||  return 1
      done
}

setup_runtime
