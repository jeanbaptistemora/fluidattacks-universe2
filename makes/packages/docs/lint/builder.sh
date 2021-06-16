# shellcheck shell=bash

function main {
  lint_markdown "${envSrcDocsDevelopment}" \
    && lint_markdown "${envSrcDocsAbout}" \
    && lint_markdown "${envSrcDocsSquad}" \
    && lint_markdown "${envSrcDocsMachine}" \
    && lint_markdown "${envSrcDocsCriteriaCompliance}" \
    && lint_markdown "${envSrcDocsCriteriaRequirementsArchitecture}" \
    && lint_markdown "${envSrcDocsCriteriaRequirementsAuthentication}" \
    && lint_markdown "${envSrcDocsCriteriaRequirementsAuthorization}" \
    && touch "${out}"
}

main "${@}"
