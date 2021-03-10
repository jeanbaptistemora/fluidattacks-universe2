import type { DocumentNode } from "graphql";
import gql from "graphql-tag";

const GET_FINDINGS: DocumentNode = gql`
  query GetFindingsQuery($projectName: String!) {
    project(projectName: $projectName) {
      findings {
        id
        age
        lastVulnerability
        type
        title
        description
        severityScore
        openAge
        openVulnerabilities
        state
        isExploitable
        remediated
        verified
        vulnerabilities(state: "open") {
          historicTreatment {
            date
            user
            treatment
          }
          where
          zeroRisk
        }
      }
    }
  }
`;

const REQUEST_PROJECT_REPORT: DocumentNode = gql`
  query RequestProjectReport(
    $reportType: ReportType!
    $projectName: String!
    $lang: ReportLang
  ) {
    report(reportType: $reportType, projectName: $projectName, lang: $lang) {
      url
    }
  }
`;

export { GET_FINDINGS, REQUEST_PROJECT_REPORT };
