import type { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FINDING_VULN_INFO: DocumentNode = gql`
  query GetFindingVulnInfo($findingId: String!, $groupName: String!) {
    finding(identifier: $findingId) {
      id
      newRemediated
      state
      verified
      vulnerabilities {
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
        tag
        verification
        vulnType
        where
        zeroRisk
      }
    }
    project(projectName: $groupName) {
      subscription
    }
  }
`;
