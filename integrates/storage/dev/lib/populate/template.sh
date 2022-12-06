# shellcheck shell=bash

function _deploy_infra {
  deploy_infra="${1}"

  if [ "${deploy_infra}" == "true" ]; then
    deploy-terraform-for-integratesStorageDev
  elif [ "${deploy_infra}" == "false" ]; then
    info "Skipping infra deployment."
  else
    error "Must provide either 'true' or 'false'."
  fi
}

function _prepare_data {
  local data="${1}"
  local branch="${2}"
  local bill_year
  local bill_month

  : \
    && bill_year="$(date +'%Y')" \
    && bill_month="$(date +'%m')" \
    && mv \
      "${data}/analytics/branch" \
      "${data}/analytics/${branch}" \
    && mv \
      "${data}/continuous-data/bills/year" \
      "${data}/continuous-data/bills/${bill_year}" \
    && mv \
      "${data}/continuous-data/bills/${bill_year}/month" \
      "${data}/continuous-data/bills/${bill_year}/${bill_month}"
}

function populate {
  local deploy_infra="${1:-true}"
  local sync_path="${2:-}"
  local data="__argData__"
  local mutable_data
  local branch
  local endpoint

  : \
    && branch="${CI_COMMIT_REF_NAME}" \
    && _deploy_infra "${deploy_infra}" \
    && mutable_data="$(mktemp -d)" \
    && copy "${data}" "${mutable_data}" \
    && _prepare_data "${mutable_data}" "${branch}" \
    && endpoint="integrates.${branch}" \
    && aws_s3_sync \
      "${mutable_data}" \
      "s3://${endpoint}${sync_path}" \
      --size-only \
      --delete \
    && rm -rf "${mutable_data}" \
    || return 1
}
