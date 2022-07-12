import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_TODO_REATTACKS: DocumentNode = gql`
  query GetTodoReattacks {
    me {
      userEmail
      organizations {
        name
        groups {
          name
          findings(filters: { verified: false }) {
            id
            age
            groupName
            lastVulnerability
            openVulnerabilities
            severityScore
            state
            title
          }
        }
      }
    }
  }
`;
