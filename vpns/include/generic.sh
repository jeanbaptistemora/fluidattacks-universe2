#! /usr/bin/env bash
# shellcheck disable=SC2024

function get_subs {
  local subs

      subs=$(basename "${0%.*}") \
  &&  subs="${subs%-*}" \
  &&  echo "${subs}"
}

function get_secret {
  # Read a var from secrets.yaml and echo its value to stdout
  local variable="${1}"
  local secrets
  local subs

      subs="$(get_subs)" \
  &&  secrets="subscriptions/${subs}/config/secrets.yaml" \
  &&  sops \
        --aws-profile "continuous-${subs}" \
        -d \
        --extract "[\"${variable}\"]" \
        "${secrets}"
}

function okta_aws_login {
  local subs
  export AWS_PROFILE

      subs="$(get_subs)" \
  &&  toolbox \
        --okta-aws-login \
        --subs "${subs}" \
  &&  AWS_PROFILE="continuous-${subs}"
}
