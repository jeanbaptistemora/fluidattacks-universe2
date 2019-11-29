import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_EVENT_DESCRIPTION: DocumentNode = gql`
  query GetEventDescription($eventId: String!) {
    event(identifier: $eventId) {
      accessibility
      affectation
      affectedComponents
      analyst
      client
      detail
      id
    }
  }
`;

export const UPDATE_DESCRIPTION_MUTATION: DocumentNode = gql`
  mutation UpdateDescriptionMutation($eventId: String!, $affectation: String!) {
    updateEvent(eventId: $eventId, affectation: $affectation) {
      success
    }
  }
`;
