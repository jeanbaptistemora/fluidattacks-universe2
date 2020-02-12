import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const HANDLE_ACCEPTATION: DocumentNode = gql
  `mutation HandleAcceptation($findingId: String!, $observations: String!, $projectName: String!, $response: String!) {
    handleAcceptation(
      findingId: $findingId,
      observations: $observations,
      projectName: $projectName,
      response: $response
    ) {
      success
    }
  }`;

export const REQUEST_VERIFICATION: DocumentNode = gql`
  mutation RequestVerification ($findingId: String!, $justification: String!) {
    requestVerification(
      findingId: $findingId,
      justification: $justification
    ) {
      success
    }
  }
`;

export const VERIFY_FINDING: DocumentNode = gql`
  mutation VerifyFinding ($findingId: String!, $justification: String!) {
    verifyFinding(
      findingId: $findingId,
      justification: $justification
    ) {
      success
    }
  }
`;
