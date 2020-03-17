import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_EVENT_DESCRIPTION: DocumentNode = gql`
  query GetEventDescription($eventId: String!) {
    event(identifier: $eventId) {
      accessibility
      affectation
      affectedComponents
      analyst
      client
      detail
      eventStatus
      id
    }
  }
`;

export const UPDATE_DESCRIPTION_MUTATION: DocumentNode = gql`
  mutation UpdateEventDescriptionMutation($eventId: String!, $affectation: String!) {
    updateEvent(eventId: $eventId, affectation: $affectation) {
      success
    }
  }
`;

export const SOLVE_EVENT_MUTATION: DocumentNode = gql`
  mutation SolveEventMutation($eventId: String!, $affectation: String!, $date: DateTime!) {
    solveEvent(eventId: $eventId, affectation: $affectation, date: $date) {
      success
    }
  }
`;
