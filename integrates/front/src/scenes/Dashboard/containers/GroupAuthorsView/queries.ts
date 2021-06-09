import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_BILL: DocumentNode = gql`
  query GetBill($date: DateTime, $groupName: String!) {
    group(groupName: $groupName) {
      bill(date: $date) {
        developers {
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
