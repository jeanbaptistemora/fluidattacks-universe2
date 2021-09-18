import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FINDINGS: DocumentNode = gql`
  query GetFindingsQuery($groupName: String!) {
    group(groupName: $groupName) {
      findings {
        id
        age
        lastVulnerability
        lastVulnerabilityReportDate
        title
        description
        severityScore
        oldestOpenVulnerabilityReportDate
        openVulnerabilities
        state
        isExploitable
        remediated
        treatmentSummary {
          accepted
          acceptedUndefined
          inProgress
          new
        }
        verified
        where
      }
      name
    }
  }
`;

const REQUEST_GROUP_REPORT: DocumentNode = gql`
  query RequestGroupReport(
    $reportType: ReportType!
    $groupName: String!
    $lang: ReportLang
  ) {
    report(reportType: $reportType, groupName: $groupName, lang: $lang) {
      url
    }
  }
`;

export { GET_FINDINGS, REQUEST_GROUP_REPORT };
