import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FINDING_VULN_INFO: DocumentNode = gql`
  query GetFindingVulnInfo(
    $findingId: String!,
    $groupName: String!
  ) {
    finding(identifier: $findingId) {
      id
      newRemediated
      state
      verified
      vulnerabilities {
        id
        specific
        where
        historicTreatment {
          acceptanceStatus
          treatment
        }
      }
    }
    project(projectName: $groupName) {
      subscription
    }
  }
`;
