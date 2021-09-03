import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_EVENT_DESCRIPTION: DocumentNode = gql`
  query GetEventDescription($eventId: String!) {
    event(identifier: $eventId) {
      accessibility
      affectation
      affectedComponents
      client
      detail
      eventStatus
      hacker
      id
    }
  }
`;

const SOLVE_EVENT_MUTATION: DocumentNode = gql`
  mutation SolveEventMutation(
    $eventId: String!
    $affectation: String!
    $date: DateTime!
  ) {
    solveEvent(eventId: $eventId, affectation: $affectation, date: $date) {
      success
    }
  }
`;

export { GET_EVENT_DESCRIPTION, SOLVE_EVENT_MUTATION };
