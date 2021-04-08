import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_EVENT_CONSULTING: DocumentNode = gql`
  query GetEventConsulting($eventId: String!) {
    event(identifier: $eventId) {
      consulting {
        id
        content
        created
        email
        fullname
        modified
        parent
      }
      id
    }
  }
`;

const ADD_EVENT_CONSULT: DocumentNode = gql`
  mutation AddEventConsult(
    $content: String!
    $eventId: String!
    $parent: GenericScalar!
  ) {
    addEventConsult(content: $content, eventId: $eventId, parent: $parent) {
      commentId
      success
    }
  }
`;

export { GET_EVENT_CONSULTING, ADD_EVENT_CONSULT };
