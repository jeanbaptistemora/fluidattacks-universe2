import type { DocumentNode } from "graphql";
import gql from "graphql-tag";

const VULNS_FRAGMENT: DocumentNode = gql`
  fragment vulnFields on Vulnerability {
    analyst @include(if: $canRetrieveAnalyst)
    commitHash
    currentState
    cycles
    efficacy
    externalBts
    findingId
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
    vulnType
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
      newRemediated
      state
      verified
      vulnerabilities {
        ...vulnFields
      }
      zeroRisk @include(if: $canRetrieveZeroRisk) {
        ...vulnFields
      }
    }
    project(projectName: $groupName) {
      subscription
    }
  }
  ${VULNS_FRAGMENT}
`;
