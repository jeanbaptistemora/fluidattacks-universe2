import { gql } from "apollo-boost";
import { DocumentNode } from "graphql";

export const GET_EVENTS: DocumentNode = gql`
  query GetEventsQuery($projectName: String!) {
    events(projectName: $projectName){
      eventDate,
      detail,
      id,
      projectName,
      eventStatus,
      eventType
    }
  }
`;
