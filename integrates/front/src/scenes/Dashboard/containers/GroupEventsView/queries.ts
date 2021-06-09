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
      }
      name
    }
  }
`;

const CREATE_EVENT_MUTATION: DocumentNode = gql`
  mutation CreateEventMutation(
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
    createEvent(
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
      projectName: $groupName
    ) {
      success
    }
  }
`;

export { CREATE_EVENT_MUTATION, GET_EVENTS };
