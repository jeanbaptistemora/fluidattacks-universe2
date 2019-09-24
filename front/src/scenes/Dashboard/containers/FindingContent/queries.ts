import { DocumentNode, gql } from "apollo-boost";
import _ from "lodash";

const userRole: string = (window as typeof window & { userRole: string }).userRole;

export const GET_FINDING_HEADER: DocumentNode = gql`
  query GetFindingHeader($findingId: String!) {
    finding(identifier: $findingId) {
      analyst @include(if: ${_.includes(["admin", "analyst"], userRole)})
      id
      reportDate
      title
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
