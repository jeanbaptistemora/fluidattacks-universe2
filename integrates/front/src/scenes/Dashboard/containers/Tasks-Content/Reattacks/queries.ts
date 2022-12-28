import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_TODO_REATTACKS: DocumentNode = gql`
  query GetTodoReattacksOPEN {
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
