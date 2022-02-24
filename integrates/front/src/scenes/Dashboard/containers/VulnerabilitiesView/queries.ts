import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const VULNS_FRAGMENT: DocumentNode = gql`
  fragment vulnFields on Vulnerability {
    currentState
    externalBugTrackingSystem
    findingId
    id
    lastTreatmentDate
    lastVerificationDate
    remediated
    reportDate
    severity
    specific
    stream
    tag
    treatment
    treatmentAcceptanceDate
    treatmentAcceptanceStatus
    treatmentAssigned
    treatmentJustification
    treatmentUser
    verification
    vulnerabilityType
    where
    zeroRisk
  }
`;

const GET_FINDING_AND_GROUP_INFO: DocumentNode = gql`
  query GetFindingInfo($findingId: String!) {
    finding(identifier: $findingId) {
      id
      remediated
      releaseDate
      state
      verified
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

export { VULNS_FRAGMENT, GET_FINDING_AND_GROUP_INFO, GET_FINDING_VULNS };
