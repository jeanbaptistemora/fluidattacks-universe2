import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_REATTACK_VULNS: DocumentNode = gql`
  query GetReattackVulns($groupName: String!) {
    group(groupName: $groupName) {
      findings {
        id
        title
        vulnerabilitiesToReattack {
          findingId
          id
          where
          specific
        }
      }
      name
    }
  }
`;

export { GET_REATTACK_VULNS };
