terraform_states_bucket() {

  # Creates states bucket for all terraform modules

  set -e

  ./services/states-bucket/states-bucket.sh

}

terraform_states_bucket
