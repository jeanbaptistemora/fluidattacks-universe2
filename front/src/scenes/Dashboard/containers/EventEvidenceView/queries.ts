import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_EVENT_EVIDENCES: DocumentNode = gql`
  query GetEventEvidences($eventId: String!) {
    event(identifier: $eventId) {
      evidence
      id
    }
  }
`;

export const UPDATE_EVIDENCE_MUTATION: DocumentNode = gql`
  mutation UpdateEvidenceMutation($eventId: String!, $file: Upload!) {
    updateEventEvidence(eventId: $eventId, file: $file) {
      success
    }
  }
`;
