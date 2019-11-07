import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_EVENTS: DocumentNode = gql`
  query GetEventsQuery($projectName: String!) {
    project(projectName: $projectName) {
      events {
        eventDate
        detail
        id
        projectName
        eventStatus
        eventType
      }
    }
  }
`;

export const CREATE_EVENT_MUTATION: DocumentNode = gql`
  mutation CreateEventMutation(
    $accessibility: [EventAccessibility]!,
    $actionAfterBlocking: ActionsAfterBlocking!,
    $actionBeforeBlocking: ActionsBeforeBlocking!,
    $affectedComponents: [AffectedComponents],
    $blockingHours: Int,
    $clientResponsible: String!,
    $context: EventContext!,
    $detail: String!,
    $eventDate: DateTime!,
    $eventType: EventType!,
    $projectName: String!
    ) {
    createEvent(
      accessibility: $accessibility,
      actionAfterBlocking: $actionAfterBlocking,
      actionBeforeBlocking: $actionBeforeBlocking,
      affectedComponents: $affectedComponents,
      blockingHours: $blockingHours,
      clientResponsible: $clientResponsible,
      context: $context,
      detail: $detail,
      eventDate: $eventDate,
      eventType: $eventType,
      projectName: $projectName
    ) {
      success
    }
  }
`;
