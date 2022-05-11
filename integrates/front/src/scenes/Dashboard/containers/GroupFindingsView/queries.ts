import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FINDINGS: DocumentNode = gql`
  query GetFindingsQuery($groupName: String!) {
    group(groupName: $groupName) {
      findings {
        id
        age
        closedVulnerabilities
        lastVulnerability
        title
        description
        severityScore
        openAge
        openVulnerabilities
        state
        minTimeToRemediate
        isExploitable
        releaseDate
        remediated
        treatmentSummary {
          accepted
          acceptedUndefined
          inProgress
          new
        }
        verificationSummary {
          onHold
          requested
          verified
        }
        verified
      }
      name
      businessId
      businessName
      description
      userRole
    }
  }
`;

const REQUEST_GROUP_REPORT: DocumentNode = gql`
  query RequestGroupReport(
    $reportType: ReportType!
    $groupName: String!
    $lang: ReportLang
    $treatments: [VulnerabilityTreatment!]
    $verificationCode: String!
  ) {
    report(
      reportType: $reportType
      groupName: $groupName
      lang: $lang
      treatments: $treatments
      verificationCode: $verificationCode
    ) {
      success
    }
  }
`;

export { GET_FINDINGS, REQUEST_GROUP_REPORT };
