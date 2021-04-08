import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const DOWNLOAD_FILE_MUTATION: DocumentNode = gql`
  mutation DownloadEventFileMutation($eventId: String!, $fileName: String!) {
    downloadEventFile(eventId: $eventId, fileName: $fileName) {
      success
      url
    }
  }
`;

const GET_EVENT_EVIDENCES: DocumentNode = gql`
  query GetEventEvidences($eventId: String!) {
    event(identifier: $eventId) {
      eventStatus
      evidence
      evidenceDate
      evidenceFile
      evidenceFileDate
      id
    }
  }
`;

const UPDATE_EVIDENCE_MUTATION: DocumentNode = gql`
  mutation UpdateEventEvidenceMutation(
    $eventId: String!
    $evidenceType: EventEvidenceType!
    $file: Upload!
  ) {
    updateEventEvidence(
      eventId: $eventId
      evidenceType: $evidenceType
      file: $file
    ) {
      success
    }
  }
`;

const REMOVE_EVIDENCE_MUTATION: DocumentNode = gql`
  mutation RemoveEventEvidenceMutation(
    $eventId: String!
    $evidenceType: EventEvidenceType!
  ) {
    removeEventEvidence(eventId: $eventId, evidenceType: $evidenceType) {
      success
    }
  }
`;

export {
  DOWNLOAD_FILE_MUTATION,
  GET_EVENT_EVIDENCES,
  UPDATE_EVIDENCE_MUTATION,
  REMOVE_EVIDENCE_MUTATION,
};
