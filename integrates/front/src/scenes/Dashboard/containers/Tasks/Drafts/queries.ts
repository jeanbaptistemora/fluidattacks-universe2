import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_TODO_DRAFTS: DocumentNode = gql`
  query GetTodoDrafts {
    me {
      userEmail
      organizations {
        name
        groups {
          name
          drafts {
            currentState
            groupName
            hacker
            id
            openVulnerabilities
            reportDate
            severityScore
            title
          }
        }
      }
    }
  }
`;
