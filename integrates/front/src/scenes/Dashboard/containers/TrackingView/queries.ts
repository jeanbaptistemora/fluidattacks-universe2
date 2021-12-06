import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_FINDING_TRACKING: DocumentNode = gql`
  query GetFindingTracking($findingId: String!) {
    finding(identifier: $findingId) {
      tracking {
        accepted
        acceptedUndefined
        assigned
        closed
        cycle
        date
        justification
        open
      }
      id
    }
  }
`;
