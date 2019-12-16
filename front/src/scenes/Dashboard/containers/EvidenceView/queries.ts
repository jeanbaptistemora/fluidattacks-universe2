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
  mutation UpdateEvidenceMutation($evidenceId: String!, $file: Upload!, $findingId: String!) {
    updateEvidence(evidenceId: $evidenceId, file: $file, findingId: $findingId) {
      success
    }
  }
`;

export const UPDATE_DESCRIPTION_MUTATION: DocumentNode = gql`
  mutation UpdateDescriptionMutation($description: String!, $field: String!, $findingId: String!) {
    updateEvidenceDescription(description: $description, field: $field, findingId: $findingId) {
      success
    }
  }
`;
