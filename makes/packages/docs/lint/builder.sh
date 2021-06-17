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
    && lint_markdown "${envSrcDocsCriteriaRequirementsCertificates}" \
    && lint_markdown "${envSrcDocsCriteriaRequirementsCredentials}" \
    && lint_markdown "${envSrcDocsCriteriaRequirementsCryptography}" \
    && lint_markdown "${envSrcDocsCriteriaRequirementsData}" \
    && lint_markdown "${envSrcDocsCriteriaRequirementsDevices}" \
    && lint_markdown "${envSrcDocsCriteriaRequirementsEmails}" \
    && lint_markdown "${envSrcDocsCriteriaRequirementsFiles}" \
    && lint_markdown "${envSrcDocsCriteriaRequirementsLegal}" \
    && touch "${out}"
}

main "${@}"
