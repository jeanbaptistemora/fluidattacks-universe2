# shellcheck shell=bash

function main {
  lint_markdown "${envSrcDocsDevelopment}" \
    && lint_markdown "${envSrcDocsAbout}" \
    && lint_markdown "${envSrcDocsSquad}" \
    && lint_markdown "${envSrcDocsMachine}" \
    && touch "${out}"
}

main "${@}"
