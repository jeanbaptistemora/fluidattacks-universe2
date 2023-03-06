import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_EVENTS: DocumentNode = gql`
  query GetEventsQuery($groupName: String!) {
    group(groupName: $groupName) {
      events {
        eventDate
        detail
        id
        groupName
        eventStatus
        eventType
        closingDate
        root {
          ... on GitRoot {
            id
            nickname
          }
          ... on URLRoot {
            id
            nickname
          }
          ... on IPRoot {
            id
            nickname
          }
        }
      }
      name
    }
  }
`;

const ADD_EVENT_MUTATION: DocumentNode = gql`
  mutation AddEventMutation(
    $detail: String!
    $eventDate: DateTime!
    $eventType: EventType!
    $groupName: String!
    $rootId: ID
  ) {
    addEvent(
      detail: $detail
      eventDate: $eventDate
      eventType: $eventType
      groupName: $groupName
      rootId: $rootId
    ) {
      eventId
      success
    }
  }
`;

const REQUEST_EVENT_VERIFICATION_MUTATION: DocumentNode = gql`
  mutation RequestEventVerification($eventId: String!, $comments: String!) {
    requestEventVerification(eventId: $eventId, comments: $comments) {
      success
    }
  }
`;

const REQUEST_VULNS_HOLD_MUTATION: DocumentNode = gql`
  mutation RequestVulnerabilitiesHold(
    $eventId: String!
    $findingId: String!
    $groupName: String!
    $vulnerabilities: [String!]!
  ) {
    requestVulnerabilitiesHold(
      eventId: $eventId
      findingId: $findingId
      groupName: $groupName
      vulnerabilities: $vulnerabilities
    ) {
      success
    }
  }
`;

export {
  ADD_EVENT_MUTATION,
  GET_EVENTS,
  REQUEST_EVENT_VERIFICATION_MUTATION,
  REQUEST_VULNS_HOLD_MUTATION,
};
