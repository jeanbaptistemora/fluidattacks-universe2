import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_BILL: DocumentNode = gql`
  query GetBill($date: DateTime, $projectName: String!) {
    group(groupName: $projectName) {
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
