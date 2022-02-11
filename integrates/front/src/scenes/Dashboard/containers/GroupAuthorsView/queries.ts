import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_BILLING: DocumentNode = gql`
  query GetBilling($date: DateTime, $groupName: String!) {
    group(groupName: $groupName) {
      billing(date: $date) {
        authors {
          actor
          commit
          groups
          organization
          repository
        }
      }
      name
    }
  }
`;
