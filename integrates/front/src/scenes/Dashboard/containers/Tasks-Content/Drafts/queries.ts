import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_TODO_DRAFTS: DocumentNode = gql`
  query GetTodoDrafts {
    me {
      drafts {
        currentState
        groupName
        hacker
        id
        lastStateDate
        openVulnerabilities
        reportDate
        severityScore
        title
      }
      userEmail
    }
  }
`;
