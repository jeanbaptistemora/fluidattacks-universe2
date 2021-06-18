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
    && lint_markdown "${envSrcDocsCriteriaRequirementsLogs}" \
    && lint_markdown "${envSrcDocsCriteriaRequirementsNetworks}" \
    && lint_markdown "${envSrcDocsCriteriaRequirementsPrivacy}" \
    && lint_markdown "${envSrcDocsCriteriaRequirementsServices}" \
    && lint_markdown "${envSrcDocsCriteriaRequirementsSession}" \
    && lint_markdown "${envSrcDocsCriteriaRequirementsSocial}" \
    && lint_markdown "${envSrcDocsCriteriaVulnerabilities}" \
    && touch "${out}"
}

main "${@}"
