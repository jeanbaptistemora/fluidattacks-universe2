import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_EVENT_COMMENTS: DocumentNode = gql`
  query GetEventComments($eventId: String!) {
    event(identifier: $eventId) {
      comments {
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

export const ADD_EVENT_COMMENT: DocumentNode = gql`
  mutation AddEventComment(
    $content: String!, $eventId: String!, $parent: GenericScalar!
  ) {
    addEventComment(content: $content, eventId: $eventId, parent: $parent) {
      commentId
      success
    }
  }
`;
