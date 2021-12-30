import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_VULN_ADDITIONAL_INFO: DocumentNode = gql`
  query GetVulnAdditionalInfo($vulnId: String!) {
    vulnerability(uuid: $vulnId) {
      cycles
    }
  }
`;

export { GET_VULN_ADDITIONAL_INFO };
