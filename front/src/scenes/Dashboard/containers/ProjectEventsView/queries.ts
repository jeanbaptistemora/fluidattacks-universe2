import { gql } from "apollo-boost";
import { DocumentNode } from "graphql";

export const GET_EVENTS: DocumentNode = gql`
  query GetEventsQuery($projectName: String!) {
    project(projectName: $projectName) {
      events {
        eventDate
        detail
        id
        projectName
        eventStatus
        eventType
      }
    }
  }
`;
