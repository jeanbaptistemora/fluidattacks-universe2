import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_VULN_TREATMENT: DocumentNode = gql`
  query GetVulnTreatment($vulnId: String!) {
    vulnerability(uuid: $vulnId) {
      historicTreatment {
        acceptanceDate
        acceptanceStatus
        assigned
        date
        justification
        user
        treatment
      }
    }
  }
`;

export { GET_VULN_TREATMENT };
