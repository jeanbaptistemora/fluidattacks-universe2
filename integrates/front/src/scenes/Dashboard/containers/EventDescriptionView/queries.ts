/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_EVENT_DESCRIPTION: DocumentNode = gql`
  query GetEventDescription($eventId: String!) {
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
      hacker
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
  mutation UpdateEventMutation($eventId: String!, $eventType: EventType) {
    updateEvent(eventId: $eventId, eventType: $eventType) {
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
  REJECT_EVENT_SOLUTION_MUTATION,
  SOLVE_EVENT_MUTATION,
  UPDATE_EVENT_MUTATION,
  UPDATE_EVENT_SOLVING_REASON_MUTATION,
};
