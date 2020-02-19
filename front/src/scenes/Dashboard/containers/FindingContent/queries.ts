import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FINDING_HEADER: DocumentNode = gql`
  query GetFindingHeader($findingId: String!, $submissionField: Boolean!) {
    finding(identifier: $findingId) {
      closedVulns: closedVulnerabilities
      id
      openVulns: openVulnerabilities
      releaseDate
      reportDate
      severityScore
      state
      title
      historicState @include(if: $submissionField)
    }
  }
`;

export const SUBMIT_DRAFT_MUTATION: DocumentNode = gql`
  mutation SubmitDraftMutation($findingId: String!) {
    submitDraft(findingId: $findingId) {
      success
    }
  }
`;

export const APPROVE_DRAFT_MUTATION: DocumentNode = gql`
  mutation ApproveDraftMutation($findingId: String!) {
    approveDraft(draftId: $findingId) {
      success
    }
  }
`;

export const REJECT_DRAFT_MUTATION: DocumentNode = gql`
  mutation SubmitDraftMutation($findingId: String!) {
    rejectDraft(findingId: $findingId) {
      success
    }
  }
`;
