import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_TODO_EVENTS: DocumentNode = gql`
  query GetTodoEvents {
    me {
      userEmail
      pendingEvents {
        eventDate
        detail
        id
        groupName
        eventStatus
        eventType
        root {
          ... on GitRoot {
            id
            nickname
          }

          ... on URLRoot {
            id
            nickname
          }
          ... on IPRoot {
            id
            nickname
          }
        }
      }
    }
  }
`;
