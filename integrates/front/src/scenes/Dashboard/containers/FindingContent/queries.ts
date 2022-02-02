import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FINDING_HEADER: DocumentNode = gql`
  query GetFindingHeader($findingId: String!, $canGetHistoricState: Boolean!) {
    finding(identifier: $findingId) {
      closedVulns: closedVulnerabilities
      id
      openVulns: openVulnerabilities
      releaseDate
      severityScore
      state
      title
      minTimeToRemediate
      historicState @include(if: $canGetHistoricState)
    }
  }
`;

const SUBMIT_DRAFT_MUTATION: DocumentNode = gql`
  mutation SubmitDraftMutation($findingId: String!) {
    submitDraft(findingId: $findingId) {
      success
    }
  }
`;

const APPROVE_DRAFT_MUTATION: DocumentNode = gql`
  mutation ApproveDraftMutation($findingId: String!) {
    approveDraft(draftId: $findingId) {
      success
    }
  }
`;

const REJECT_DRAFT_MUTATION: DocumentNode = gql`
  mutation RejectDraftMutation($findingId: String!) {
    rejectDraft(findingId: $findingId) {
      success
    }
  }
`;

const REMOVE_FINDING_MUTATION: DocumentNode = gql`
  mutation RemoveFindingMutation(
    $findingId: String!
    $justification: RemoveFindingJustification!
  ) {
    removeFinding(findingId: $findingId, justification: $justification) {
      success
    }
  }
`;

export {
  GET_FINDING_HEADER,
  SUBMIT_DRAFT_MUTATION,
  APPROVE_DRAFT_MUTATION,
  REJECT_DRAFT_MUTATION,
  REMOVE_FINDING_MUTATION,
};
