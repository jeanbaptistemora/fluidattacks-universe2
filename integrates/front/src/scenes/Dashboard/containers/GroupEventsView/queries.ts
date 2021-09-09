import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_EVENTS: DocumentNode = gql`
  query GetEventsQuery($groupName: String!) {
    group(groupName: $groupName) {
      events {
        accessibility
        actionAfterBlocking
        actionBeforeBlocking
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
    $actionAfterBlocking: ActionsAfterBlocking!
    $actionBeforeBlocking: ActionsBeforeBlocking!
    $affectedComponents: [AffectedComponents]
    $blockingHours: String
    $context: EventContext!
    $detail: String!
    $eventDate: DateTime!
    $eventType: EventType!
    $file: Upload
    $image: Upload
    $groupName: String!
  ) {
    addEvent(
      accessibility: $accessibility
      actionAfterBlocking: $actionAfterBlocking
      actionBeforeBlocking: $actionBeforeBlocking
      affectedComponents: $affectedComponents
      blockingHours: $blockingHours
      context: $context
      detail: $detail
      eventDate: $eventDate
      eventType: $eventType
      file: $file
      image: $image
      groupName: $groupName
    ) {
      success
    }
  }
`;

export { ADD_EVENT_MUTATION, GET_EVENTS };
