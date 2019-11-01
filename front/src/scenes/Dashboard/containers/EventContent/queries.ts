import { DocumentNode, gql } from "apollo-boost";

export const GET_EVENT_HEADER: DocumentNode = gql`
  query GetEventHeader($eventId: String!) {
    event(identifier: $eventId) {
      eventDate
      eventStatus
      eventType
      id
    }
  }
`;
