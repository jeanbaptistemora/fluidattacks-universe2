import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FINDINGS: DocumentNode = gql`
  query GetFindingsQuery($projectName: String!) {
    group(projectName: $projectName) {
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
      name
    }
  }
`;

const REQUEST_GROUP_REPORT: DocumentNode = gql`
  query RequestGroupReport(
    $reportType: ReportType!
    $projectName: String!
    $lang: ReportLang
  ) {
    report(reportType: $reportType, projectName: $projectName, lang: $lang) {
      url
    }
  }
`;

export { GET_FINDINGS, REQUEST_GROUP_REPORT };
