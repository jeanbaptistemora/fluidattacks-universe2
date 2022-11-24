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

function main {
  local data="__argData__"
  local tmp
  local branch
  local endpoint

  : \
    && branch="${CI_COMMIT_REF_NAME}" \
    && deploy-terraform-for-integratesStorageDev \
    && tmp="$(mktemp -d)" \
    && copy "${data}" "${tmp}" \
    && _prepare_data "${tmp}" "${branch}" \
    && endpoint="integrates.${branch}" \
    && aws_s3_sync \
      "${data}" \
      "s3://${endpoint}" \
      --delete \
    || return 1
}

main "${@}"
