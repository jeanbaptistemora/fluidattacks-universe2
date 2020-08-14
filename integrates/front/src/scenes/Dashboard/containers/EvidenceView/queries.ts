import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FINDING_EVIDENCES: DocumentNode = gql`
  query GetFindingEvidences($findingId: String!) {
    finding(identifier: $findingId) {
      evidence
      id
    }
  }
`;

export const UPDATE_EVIDENCE_MUTATION: DocumentNode = gql`
  mutation UpdateEvidenceMutation($evidenceId: EvidenceType!, $file: Upload!, $findingId: String!) {
    updateEvidence(evidenceId: $evidenceId, file: $file, findingId: $findingId) {
      success
    }
  }
`;

export const UPDATE_DESCRIPTION_MUTATION: DocumentNode = gql`
  mutation UpdateDescriptionMutation(
    $description: String!, $evidenceId: EvidenceDescriptionType!, $findingId: String!
  ) {
    updateEvidenceDescription(description: $description, evidenceId: $evidenceId, findingId: $findingId) {
      success
    }
  }
`;

export const REMOVE_EVIDENCE_MUTATION: DocumentNode = gql`
  mutation RemoveEvidenceMutation($evidenceId: EvidenceType!, $findingId: String!) {
    removeEvidence(evidenceId: $evidenceId, findingId: $findingId) {
      success
    }
  }
`;
