# shellcheck shell=bash

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

function populate_storage {
  local sync_path="${1:-}"
  local data="__argData__"
  local endpoint="integrates.dev"
  local mutable_data
  local branch

  : \
    && branch="${CI_COMMIT_REF_NAME}" \
    && mutable_data="$(mktemp -d)" \
    && copy "${data}" "${mutable_data}" \
    && _prepare_data "${mutable_data}" "${branch}" \
    && aws_s3_sync \
      "${mutable_data}" \
      "s3://${endpoint}${sync_path}" \
      --size-only \
      --delete \
      "${@:2}" \
    && rm -rf "${mutable_data}"
}
