import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FINDING_HEADER: DocumentNode = gql`
  query GetFindingHeader($findingId: String!) {
    finding(identifier: $findingId) {
      closedVulns: closedVulnerabilities
      id
      openVulns: openVulnerabilities
      releaseDate
      reportDate
      title
      submissionHistory
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
