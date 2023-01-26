import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_TODO_REATTACKS: DocumentNode = gql`
  query GetTodoReattacksVulnerable($after: String, $first: Int) {
    me {
      findingReattacksConnection(after: $after, first: $first) {
        edges {
          node {
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
              pageInfo {
                endCursor
                hasNextPage
              }
              total
            }
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
        total
      }
      userEmail
    }
  }
`;
