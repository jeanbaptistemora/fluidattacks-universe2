import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_BILLING: DocumentNode = gql`
  query GetBilling($date: DateTime, $groupName: String!) {
    group(groupName: $groupName) {
      authors(date: $date) {
        data {
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
