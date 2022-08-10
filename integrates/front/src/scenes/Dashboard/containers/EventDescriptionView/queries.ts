import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_EVENT_DESCRIPTION: DocumentNode = gql`
  query GetEventDescription($eventId: String!) {
    event(identifier: $eventId) {
      accessibility
      affectedComponents
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
      hacker
      id
      otherSolvingReason
      solvingReason
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
    $affectedComponents: [AffectedComponents]
    $eventId: String!
    $eventType: EventType
  ) {
    updateEvent(
      affectedComponents: $affectedComponents
      eventId: $eventId
      eventType: $eventType
    ) {
      success
    }
  }
`;

const UPDATE_EVENT_SOLVING_REASON_MUTATION: DocumentNode = gql`
  mutation UpdateEventSolvingReasonMutation(
    $eventId: String!
    $other: String
    $reason: SolveEventReason!
  ) {
    updateEventSolvingReason(
      eventId: $eventId
      reason: $reason
      other: $other
    ) {
      success
    }
  }
`;

export {
  GET_EVENT_DESCRIPTION,
  SOLVE_EVENT_MUTATION,
  UPDATE_EVENT_MUTATION,
  UPDATE_EVENT_SOLVING_REASON_MUTATION,
};
