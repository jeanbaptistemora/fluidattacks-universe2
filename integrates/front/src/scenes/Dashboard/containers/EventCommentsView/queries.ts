import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_EVENT_CONSULTING: DocumentNode = gql`
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

export const ADD_EVENT_CONSULT: DocumentNode = gql`
  mutation AddEventConsult(
    $content: String!, $eventId: String!, $parent: GenericScalar!
  ) {
    addEventConsult(content: $content, eventId: $eventId, parent: $parent) {
      commentId
      success
    }
  }
`;
