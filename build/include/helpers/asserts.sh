# shellcheck shell=bash

function helper_asserts_aws_login {
  local user="${1}"
  export AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY


      if [ "${user}" = 'dev' ]
      then
            AWS_ACCESS_KEY_ID="${ASSERTS_DEV_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${ASSERTS_DEV_AWS_SECRET_ACCESS_KEY}"
      elif [ "${user}" = 'prod' ]
      then
            AWS_ACCESS_KEY_ID="${ASSERTS_PROD_AWS_ACCESS_KEY_ID}" \
        &&  AWS_SECRET_ACCESS_KEY="${ASSERTS_PROD_AWS_SECRET_ACCESS_KEY}"
      else
            echo '[ERROR] either prod or dev must be passed as arg' \
        &&  return 1
      fi \
  &&  echo "[INFO] Logging into AWS with ${user} credentials" \
  &&  aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" \
  &&  aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}" \
  &&  aws configure set region 'us-east-1'
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

function helper_with_development_secrets {
      helper_asserts_aws_login dev \
  &&  helper_common_sops_env 'secrets/development.yaml' 'default' \
        AZURE_CLIENT_ID \
        AZURE_CLIENT_SECRET \
        AZURE_SUBSCRIPTION_ID \
        AZURE_TENANT_ID \
        GOOGLE_APPLICATION_CREDENTIALS_CONTENT \
        AWS_EC2_INSTANCE \
        KUBERNETES_API_TOKEN \
        WEBBOT_GMAIL_PASS \
        WEBBOT_GMAIL_USER \
        AWS_ACCESS_KEY_ID \
        AWS_SECRET_ACCESS_KEY
}

function helper_with_production_secrets {
      helper_asserts_aws_login prod \
  &&  helper_common_sops_env 'secrets/production.yaml' 'default' \
        TWINE_USERNAME \
        TWINE_PASSWORD \
        DOCKER_HUB_USER \
        DOCKER_HUB_PASS \
        MANDRILL_APIKEY
}

function helper_asserts_mocks_ctl {
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

function helper_test_fluidasserts {
  helper_with_development_secrets

  local marker_name="${1}"

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

  helper_asserts_mocks_ctl prepare  "${marker_name}"

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
  &&  version=$(helper_asserts_version) \
  &&  checks_number=$(grep -rIE '@(track|api)' fluidasserts/ | wc -l) \
  &&  sed -i "s/<CHECKS>/${checks_number}/" sphinx/source/index.rst \
  &&  sphinx-build -D version="v.${version}" -D release="v.${version}" \
        -b dirhtml -a sphinx/source/ public/ \
  &&  sphinx-build -b linkcheck sphinx/source public/review/ \
  &&  sphinx-build -b coverage  sphinx/source public/review/
}
