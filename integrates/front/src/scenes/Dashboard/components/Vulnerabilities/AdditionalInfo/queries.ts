import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_VULN_ADDITIONAL_INFO: DocumentNode = gql`
  query GetVulnAdditionalInfo($canRetrieveHacker: Boolean!, $vulnId: String!) {
    vulnerability(uuid: $vulnId) {
      commitHash
      cycles
      efficacy
      hacker @include(if: $canRetrieveHacker)
      lastReattackRequester
      lastRequestedReattackDate
      lastStateDate
      lastTreatmentDate
      reportDate
      severity
      stream
      treatment
      treatmentAcceptanceDate
      treatmentAssigned
      treatmentChanges
      treatmentJustification
      vulnerabilityType
    }
  }
`;

export { GET_VULN_ADDITIONAL_INFO };
