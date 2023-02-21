import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_EVENT_DESCRIPTION: DocumentNode = gql`
  query GetEventDescription($canRetrieveHacker: Boolean!, $eventId: String!) {
    event(identifier: $eventId) {
      affectedReattacks {
        findingId
        where
        specific
      }
      client
      closingDate
      detail
      eventType
      eventStatus
      hacker @include(if: $canRetrieveHacker)
      id
      otherSolvingReason
      solvingReason
    }
  }
`;

const REJECT_EVENT_SOLUTION_MUTATION: DocumentNode = gql`
  mutation RejectEventSolutionMutation($eventId: String!, $comments: String!) {
    rejectEventSolution(eventId: $eventId, comments: $comments) {
      success
    }
  }
`;

const SOLVE_EVENT_MUTATION: DocumentNode = gql`
  mutation SolveEventMutation(
    $eventId: String!
    $other: String
    $reason: SolveEventReason!
  ) {
    solveEvent(eventId: $eventId, reason: $reason, other: $other) {
      success
    }
  }
`;

const UPDATE_EVENT_MUTATION: DocumentNode = gql`
  mutation UpdateEventMutation(
    $eventId: String!
    $eventType: EventType
    $otherSolvingReason: String
    $solvingReason: SolveEventReason
  ) {
    updateEvent(
      eventId: $eventId
      eventType: $eventType
      otherSolvingReason: $otherSolvingReason
      solvingReason: $solvingReason
    ) {
      success
    }
  }
`;

export {
  GET_EVENT_DESCRIPTION,
  REJECT_EVENT_SOLUTION_MUTATION,
  SOLVE_EVENT_MUTATION,
  UPDATE_EVENT_MUTATION,
};
