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
    $file: Upload
    $image: Upload
    $groupName: String!
    $rootId: ID!
  ) {
    addEvent(
      detail: $detail
      eventDate: $eventDate
      eventType: $eventType
      file: $file
      image: $image
      groupName: $groupName
      rootId: $rootId
    ) {
      eventId
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

export { ADD_EVENT_MUTATION, GET_EVENTS, REQUEST_VULNS_HOLD_MUTATION };
