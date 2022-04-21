import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_EVENTS: DocumentNode = gql`
  query GetEventsQuery($groupName: String!) {
    group(groupName: $groupName) {
      events {
        accessibility
        affectedComponents
        eventDate
        detail
        id
        groupName
        eventStatus
        eventType
        closingDate
      }
      name
    }
  }
`;

const ADD_EVENT_MUTATION: DocumentNode = gql`
  mutation AddEventMutation(
    $accessibility: [EventAccessibility]!
    $affectedComponents: [AffectedComponents]
    $blockingHours: String
    $context: EventContext!
    $detail: String!
    $eventDate: DateTime!
    $eventType: EventType!
    $file: Upload
    $image: Upload
    $groupName: String!
    $rootId: ID!
  ) {
    addEvent(
      accessibility: $accessibility
      affectedComponents: $affectedComponents
      blockingHours: $blockingHours
      context: $context
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
