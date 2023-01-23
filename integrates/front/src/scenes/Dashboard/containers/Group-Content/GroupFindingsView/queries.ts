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
        status
        minTimeToRemediate
        isExploitable
        releaseDate
        treatmentSummary {
          accepted
          acceptedUndefined
          inProgress
          untreated
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
      hasMachine
      userRole
    }
  }
`;

const REQUEST_GROUP_REPORT: DocumentNode = gql`
  query RequestGroupReport(
    $age: Int
    $reportType: ReportType!
    $groupName: String!
    $lang: ReportLang
    $lastReport: Int
    $location: String
    $minReleaseDate: DateTime
    $maxReleaseDate: DateTime
    $treatments: [VulnerabilityTreatment!]
    $states: [VulnerabilityState!]
    $verifications: [VulnerabilityVerification!]
    $closingDate: DateTime
    $maxSeverity: Float
    $minSeverity: Float
    $findingTitle: String
    $verificationCode: String!
  ) {
    report(
      age: $age
      reportType: $reportType
      findingTitle: $findingTitle
      groupName: $groupName
      lang: $lang
      lastReport: $lastReport
      location: $location
      maxReleaseDate: $maxReleaseDate
      maxSeverity: $maxSeverity
      minReleaseDate: $minReleaseDate
      minSeverity: $minSeverity
      states: $states
      treatments: $treatments
      verifications: $verifications
      closingDate: $closingDate
      verificationCode: $verificationCode
    ) {
      success
    }
  }
`;

const GET_GROUP_VULNERABILITIES: DocumentNode = gql`
  query GetGroupVulnerabilities(
    $after: String
    $first: Int
    $groupName: String!
    $root: String
  ) {
    group(groupName: $groupName) {
      name
      vulnerabilities(after: $after, first: $first, root: $root) {
        edges {
          node {
            findingId
            id
            state
            treatmentAssigned
            where
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
      }
    }
  }
`;

export { GET_FINDINGS, GET_GROUP_VULNERABILITIES, REQUEST_GROUP_REPORT };
