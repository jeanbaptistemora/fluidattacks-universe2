import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FINDINGS: DocumentNode = gql`
  query GetFindingsQuery($groupName: String!) {
    group(groupName: $groupName) {
      findings {
        id
        age
        lastVulnerability
        title
        description
        severityScore
        openAge
        openVulnerabilities
        state
        isExploitable
        releaseDate
        remediated
        treatmentSummary {
          accepted
          acceptedUndefined
          inProgress
          new
        }
        verified
      }
      name
    }
  }
`;

const GET_GROUP_VULNS: DocumentNode = gql`
  query GetGroupVulns($groupName: String!) {
    group(groupName: $groupName) {
      findings {
        id
        vulnerabilities {
          id
          where
        }
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
      success
    }
  }
`;

const GET_HAS_MOBILE_APP: DocumentNode = gql`
  query GetHasMobileApp {
    me {
      hasMobileApp
    }
  }
`;

export {
  GET_FINDINGS,
  GET_GROUP_VULNS,
  GET_HAS_MOBILE_APP,
  REQUEST_GROUP_REPORT,
};
