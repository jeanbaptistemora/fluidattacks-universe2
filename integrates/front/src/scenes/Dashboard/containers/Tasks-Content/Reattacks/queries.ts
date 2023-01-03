import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_TODO_REATTACKS: DocumentNode = gql`
  query GetTodoReattacksVulnerable {
    me {
      findingReattacks {
        groupName
        id
        title
        verificationSummary {
          requested
        }
        vulnerabilitiesToReattackConnection {
          edges {
            node {
              lastRequestedReattackDate
            }
          }
        }
      }
      userEmail
    }
  }
`;
