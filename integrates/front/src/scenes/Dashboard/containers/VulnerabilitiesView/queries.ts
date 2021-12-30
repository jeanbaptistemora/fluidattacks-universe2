import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const VULNS_FRAGMENT: DocumentNode = gql`
  fragment vulnFields on Vulnerability {
    currentState
    externalBugTrackingSystem
    findingId
    historicTreatment {
      acceptanceDate
      acceptanceStatus
      assigned
      date
      justification
      user
      treatment
    }
    id
    lastReattackDate
    lastReattackRequester
    lastRequestedReattackDate
    remediated
    reportDate
    severity
    specific
    stream
    tag
    verification
    vulnerabilityType
    where
    zeroRisk
  }
`;

const GET_FINDING_VULN_INFO: DocumentNode = gql`
  query GetFindingVulnInfo(
    $canRetrieveZeroRisk: Boolean!
    $findingId: String!
    $groupName: String!
  ) {
    finding(identifier: $findingId) {
      id
      remediated
      releaseDate
      state
      verified
      vulnerabilities {
        ...vulnFields
      }
      zeroRisk @include(if: $canRetrieveZeroRisk) {
        ...vulnFields
      }
    }
    group(groupName: $groupName) {
      name
      subscription
    }
  }
  ${VULNS_FRAGMENT}
`;

const GET_FINDING_AND_GROUP_INFO: DocumentNode = gql`
  query GetFindingAndGroupInfo($findingId: String!, $groupName: String!) {
    finding(identifier: $findingId) {
      id
      remediated
      releaseDate
      state
      verified
    }
    group(groupName: $groupName) {
      name
      subscription
    }
  }
`;

const GET_FINDING_VULNS: DocumentNode = gql`
  query GetFindingVulns($canRetrieveZeroRisk: Boolean!, $findingId: String!) {
    finding(identifier: $findingId) {
      vulnerabilities {
        ...vulnFields
      }
      zeroRisk @include(if: $canRetrieveZeroRisk) {
        ...vulnFields
      }
    }
  }
  ${VULNS_FRAGMENT}
`;

export { GET_FINDING_VULN_INFO, GET_FINDING_AND_GROUP_INFO, GET_FINDING_VULNS };
