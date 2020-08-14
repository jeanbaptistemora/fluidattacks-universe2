import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_FINDING_TRACKING: DocumentNode = gql`
  query GetFindingTracking($findingId: String!) {
    finding(identifier: $findingId) {
      tracking
      id
    }
  }
`;
