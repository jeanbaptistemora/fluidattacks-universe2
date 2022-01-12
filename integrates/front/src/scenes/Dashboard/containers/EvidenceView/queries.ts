import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FINDING_EVIDENCES: DocumentNode = gql`
  query GetFindingEvidences($findingId: String!) {
    finding(identifier: $findingId) {
      evidence {
        animation {
          date
          description
          url
        }
        evidence1 {
          date
          description
          url
        }
        evidence2 {
          date
          description
          url
        }
        evidence3 {
          date
          description
          url
        }
        evidence4 {
          date
          description
          url
        }
        evidence5 {
          date
          description
          url
        }
        exploitation {
          date
          description
          url
        }
      }
      id
    }
  }
`;

const UPDATE_EVIDENCE_MUTATION: DocumentNode = gql`
  mutation UpdateEvidenceMutation(
    $evidenceId: EvidenceType!
    $file: Upload!
    $findingId: String!
  ) {
    updateEvidence(
      evidenceId: $evidenceId
      file: $file
      findingId: $findingId
    ) {
      success
    }
  }
`;

const UPDATE_DESCRIPTION_MUTATION: DocumentNode = gql`
  mutation UpdateDescriptionMutation(
    $description: String!
    $evidenceId: EvidenceDescriptionType!
    $findingId: String!
  ) {
    updateEvidenceDescription(
      description: $description
      evidenceId: $evidenceId
      findingId: $findingId
    ) {
      success
    }
  }
`;

const REMOVE_EVIDENCE_MUTATION: DocumentNode = gql`
  mutation RemoveEvidenceMutation(
    $evidenceId: EvidenceType!
    $findingId: String!
  ) {
    removeEvidence(evidenceId: $evidenceId, findingId: $findingId) {
      success
    }
  }
`;

export {
  GET_FINDING_EVIDENCES,
  UPDATE_EVIDENCE_MUTATION,
  UPDATE_DESCRIPTION_MUTATION,
  REMOVE_EVIDENCE_MUTATION,
};
