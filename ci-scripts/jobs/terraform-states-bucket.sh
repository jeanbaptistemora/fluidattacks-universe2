# shellcheck shell=bash

terraform_states_bucket() {

  # Creates states bucket for all terraform modules

  set -e

  # Import functions
  . services/states-bucket/states-bucket.sh

  # shellcheck disable=SC2119
  create_states_bucket

}

terraform_states_bucket
