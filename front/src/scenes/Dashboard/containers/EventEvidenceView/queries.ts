import { DocumentNode, gql } from "apollo-boost";

export const GET_EVENT_EVIDENCES: DocumentNode = gql`
  query GetEventEvidences($eventId: String!) {
    event(identifier: $eventId) {
      evidence
      id
    }
  }
`;
