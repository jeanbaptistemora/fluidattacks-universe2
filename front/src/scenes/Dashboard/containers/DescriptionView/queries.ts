import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const APPROVE_ACCEPTATION: DocumentNode = gql
  `mutation ApproveAcceptation($findingId: String!, $observations: String!, $projectName: String!) {
    approveAcceptation(
      findingId: $findingId,
      observations: $observations,
      projectName: $projectName,
    ) {
      success
    }
  }`;
