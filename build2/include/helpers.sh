# shellcheck shell=bash

function helper_use_pristine_workdir {
  export WORKDIR
  export STARTDIR

  function helper_teardown_workdir {
        echo "[INFO] Deleting: ${WORKDIR}" \
    &&  rm -rf "${WORKDIR}"
  }

      echo '[INFO] Creating a pristine workdir' \
  &&  rm -rf "${WORKDIR}" \
  &&  mkdir -p "${WORKDIR}" \
  &&  echo '[INFO] Copying files to workdir' \
  &&  cp -r "${STARTDIR}/." "${WORKDIR}" \
  &&  echo '[INFO] Entering the workdir' \
  &&  pushd "${WORKDIR}" \
  &&  echo '[INFO] Running: git clean -xdf' \
  &&  git clean -xdf \
  &&  trap 'helper_teardown_workdir' 'EXIT' \
  ||  return 1
}

function helper_use_regular_workdir {
  export STARTDIR

      echo '[INFO] Entering the workdir' \
  &&  pushd "${STARTDIR}" \
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

function helper_minutes_of_month {
  local minutes_of_passed_days
  local minutes_of_passed_hours
  local minutes_of_current_hour
  local minutes_of_month

      minutes_of_passed_days=$((
        ($(TZ=GMT date +%d | sed 's/^0//') -1) * 1440
      )) \
  &&  minutes_of_passed_hours=$((
        $(TZ=GMT date +%H | sed 's/^0//') * 60
      )) \
  &&  minutes_of_current_hour=$((
        $(TZ=GMT date +%M | sed 's/^0//')
      )) \
  &&  minutes_of_month=$((
        minutes_of_passed_days +
        minutes_of_passed_hours +
        minutes_of_current_hour
      )) \
  &&  echo "${minutes_of_month}"
}

function helper_asserts_version {
  local minutes

      minutes=$(helper_minutes_of_month) \
  &&  echo "$(TZ=GMT date +%y.%m.)${minutes}"
}

function helper_build_asserts {
  local version
  local release_folder='asserts-release'

      version=$(helper_asserts_version) \
  &&  echo "Version: ${version}" \
  &&  sed -i "s/_get_version(),/'${version}',/g" setup.py \
  &&  python3 setup.py sdist --formats=gztar \
  &&  python3 setup.py bdist_wheel \
  &&  mv dist "${release_folder}"
}

function helper_config_precommit {
  export PRE_COMMIT_HOME

      mkdir -p .cache/pre-commit \
  &&  PRE_COMMIT_HOME="${PWD}/.cache/pre-commit"
}

function helper_build_nix_caches_parallel {
  local num_provisioners
  local num_provisioners_per_group
  local num_provisioners_remaining
  export lower_limit
  export upper_limit

      num_provisioners=$(find build2/provisioners/ -type f | wc -l) \
  &&  num_provisioners_per_group=$(( num_provisioners/CI_NODE_TOTAL )) \
  &&  num_provisioners_remaining=$(( num_provisioners%CI_NODE_TOTAL )) \
  &&  if [ "${num_provisioners_remaining}" -gt '0' ]
      then
        num_provisioners_per_group=$(( num_provisioners_per_group+=1 ))
      fi \
  &&  lower_limit=$(( (CI_NODE_INDEX-1)*num_provisioners_per_group )) \
  &&  upper_limit=$(( CI_NODE_INDEX*num_provisioners_per_group-1 )) \
  &&  upper_limit=$(( upper_limit > num_provisioners-1 ? num_provisioners-1 : upper_limit ))
}

function helper_list_declared_jobs {
  declare -F | sed 's/declare -f //' | grep -P '^job_[a-z_]+' | sed 's/job_//' | sort
}

function helper_list_vars_with_regex {
  local regex="${1}"
  printenv | grep -oP "${regex}" | sort
}

function helper_with_development_secrets {
  export ENCRYPTION_KEY
  helper_decrypt_and_source "${ENCRYPTION_KEY}" './secrets/development.sh.asc'
}

function helper_with_production_secrets {
  export ENCRYPTION_KEY_PROD
  helper_decrypt_and_source "${ENCRYPTION_KEY_PROD}" './secrets/production.sh.asc'
}

function helper_decrypt_and_source {
  local encryption_key="${1}"
  local encrypted_file="${2}"

  echo "Unencrypting and sourcing: ${encrypted_file}"
  # shellcheck disable=SC1090
  source <( \
    gpg \
      --batch \
      --passphrase-fd 0 \
      --decrypt "${encrypted_file}" \
    <<< "${encryption_key}")
  echo
}

function helper_test_fluidasserts {
  helper_with_development_secrets

  local marker_name="${1}"

  function mocks_ctl {
    local action="${1}"
    local marker_name="${2}"

    pytest \
        -m "${action}" \
        --asserts-module "${marker_name}" \
        --capture=no \
        --no-cov \
        --reruns 10 \
        --reruns-delay 1 \
      "test/test_others_${action}.py"
  }
  trap "mocks_ctl shutdown ${marker_name}" 'EXIT'

  function compute_needed_test_modules_for {
    grep -lrP "'${1}'" "test/test_"*
  }

  function execute_tests_for {
    local marker_name="${1}"
    local test_modules

    mapfile -t test_modules \
      < <(compute_needed_test_modules_for "${marker_name}")

    pytest \
        --cov-branch \
        --asserts-module "${marker_name}" \
        --random-order-bucket=global \
      "${test_modules[@]}"
  }

  mocks_ctl prepare  "${marker_name}"

  execute_tests_for "${marker_name}"
}

function helper_pages_striprun {
  $1 "$2" \
    | perl -pe 's/\e([^\[\]]|\[.*?[a-zA-Z]|\].*?\a)//g' \
    | tee "$2".out
}

function helper_pages_execute_example_exploits {
  export yaml_key_b64='dGVzdHN0ZXN0c3Rlc3RzdGVzdHN0ZXN0c3Rlc3RzCg=='

      mkdir resources \
  &&  cp sphinx/source/example/resources/secrets.yml ./resources/secrets.yml \
  &&  for example in sphinx/source/example/*.py; do
            helper_pages_striprun "python3" "$example" \
        ||  return 1
      done \
  &&  for example in sphinx/source/example/*.exp; do
            helper_pages_striprun "asserts" "$example" \
        ||  return 1
      done
}

function helper_pages_generate_credits {
      echo >> sphinx/source/credits.rst \
  &&  echo 'running git-fame... this may take a loooong time' \
  &&  git-fame \
        -C \
        --log=ERROR \
        --silent-progress \
        --ignore-whitespace \
        --cost=cocomo \
      | grep -viE '^total [a-z]+: [0-9]+(\.[0-9]+)?$' \
      | grep -vP '^\D+?\d+\D+?0' \
      | grep -vP 'Jane Doe' \
      | tee -a sphinx/source/credits.rst \
  &&  cat sphinx/source/credits.rst.footer >> sphinx/source/credits.rst
}

function helper_pages_generate_doc {
  local version
  local checks_number

      mkdir -p public/ \
  &&  sphinx-apidoc -efM fluidasserts -o sphinx/source \
  &&  version=$(python3 ./build/scripts/get_version.py) \
  &&  checks_number=$(grep -rIE '@(track|api)' fluidasserts/ | wc -l) \
  &&  sed -i "s/<CHECKS>/${checks_number}/" sphinx/source/index.rst \
  &&  sphinx-build -D version="v.${version}" -D release="v.${version}" \
        -b dirhtml -a sphinx/source/ public/ \
  &&  sphinx-build -b linkcheck sphinx/source public/review/ \
  &&  sphinx-build -b coverage  sphinx/source public/review/
}
