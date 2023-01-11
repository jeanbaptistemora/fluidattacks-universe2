import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_VULN_ADDITIONAL_INFO: DocumentNode = gql`
  query GetVulnAdditionalInfo($canRetrieveHacker: Boolean!, $vulnId: String!) {
    vulnerability(uuid: $vulnId) {
      closingDate
      commitHash
      cycles
      efficacy
      hacker @include(if: $canRetrieveHacker)
      id
      lastReattackRequester
      lastRequestedReattackDate
      lastStateDate
      lastTreatmentDate
      reportDate
      rootNickname
      severity
      source
      specific
      stream
      treatmentStatus
      treatmentAcceptanceStatus
      treatmentAcceptanceDate
      treatmentAssigned
      treatmentChanges
      treatmentJustification
      vulnerabilityType
      where
    }
  }
`;

const UPDATE_VULNERABILITY_DESCRIPTION: DocumentNode = gql`
  mutation UpdateVulnerabilityDescription(
    $commit: String
    $source: VulnerabilitySource
    $vulnerabilityId: ID!
  ) {
    updateVulnerabilityDescription(
      commit: $commit
      source: $source
      vulnerabilityId: $vulnerabilityId
    ) {
      success
    }
  }
`;

export { GET_VULN_ADDITIONAL_INFO, UPDATE_VULNERABILITY_DESCRIPTION };
