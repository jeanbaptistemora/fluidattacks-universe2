import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const VULNS_FRAGMENT: DocumentNode = gql`
  fragment vulnFields on Vulnerability {
    commitHash
    currentState
    cycles
    efficacy
    externalBugTrackingSystem
    findingId
    hacker @include(if: $canRetrieveAnalyst)
    historicTreatment {
      acceptanceDate
      acceptanceStatus
      date
      justification
      user
      treatment
      treatmentManager
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

export const GET_FINDING_VULN_INFO: DocumentNode = gql`
  query GetFindingVulnInfo(
    $canRetrieveAnalyst: Boolean!
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
