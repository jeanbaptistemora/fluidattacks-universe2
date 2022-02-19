import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_UNSOLVED_EVENTS: DocumentNode = gql`
  query GetUnsolvedEventsQuery($groupName: String!) {
    group(groupName: $groupName) {
      events {
        detail
        id
        eventStatus
        eventType
      }
      name
    }
  }
`;

const UPDATE_EVENT_AFFECTATIONS: DocumentNode = gql`
  mutation updateEventAffectations(
    $eventId: String!
    $findingId: String!
    $justification: String!
    $vulnerabilities: [String]!
  ) {
    updateEventAffectations(
      eventId: $eventId
      findingId: $findingId
      justification: $justification
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

export { GET_UNSOLVED_EVENTS, UPDATE_EVENT_AFFECTATIONS };
