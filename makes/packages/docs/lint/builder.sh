# shellcheck shell=bash

function main {
  lint_markdown "${envSrcDocsDevelopment}" \
    && lint_markdown "${envSrcDocsAbout}" \
    && touch "${out}"
}

main "${@}"
