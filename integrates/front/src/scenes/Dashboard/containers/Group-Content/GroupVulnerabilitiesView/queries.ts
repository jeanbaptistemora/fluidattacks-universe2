import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const VULNS_FRAGMENT: DocumentNode = gql`
  fragment vulnGroupFields on Vulnerability {
    state
    externalBugTrackingSystem
    findingId
    id
    lastTreatmentDate
    lastVerificationDate
    remediated
    reportDate
    rootNickname
    severity
    specific
    source
    stream
    tag
    treatmentAcceptanceDate
    treatmentAcceptanceStatus
    treatmentAssigned
    treatmentJustification
    treatmentStatus
    treatmentUser
    verification
    vulnerabilityType
    where
    zeroRisk
  }
`;

const GET_GROUP_VULNERABILITIES: DocumentNode = gql`
  query GetGroupVulnerabilities(
    $after: String
    $first: Int
    $groupName: String!
    $root: String
    $search: String
    $treatment: String
    $type: String
    $stateStatus: String
    $verificationStatus: String
    $zeroRisk: VulnerabilityZeroRiskStatus
  ) {
    group(groupName: $groupName) {
      name
      vulnerabilities(
        after: $after
        first: $first
        root: $root
        search: $search
        treatment: $treatment
        type: $type
        stateStatus: $stateStatus
        verificationStatus: $verificationStatus
        zeroRisk: $zeroRisk
      ) {
        edges {
          node {
            groupName
            finding {
              id
              severityScore
              title
            }
            ...vulnGroupFields
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
        total
      }
    }
  }
  ${VULNS_FRAGMENT}
`;

export { GET_GROUP_VULNERABILITIES };
