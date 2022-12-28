import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FINDING_LOCATIONS: DocumentNode = gql`
  query GetFindingLocations($after: String, $findingId: String!, $first: Int) {
    finding(identifier: $findingId) {
      __typename
      id
      vulnerabilitiesConnection(after: $after, first: $first) {
        edges {
          node {
            currentState
            id
            treatmentAssigned
            where
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
      }
    }
  }
`;

export { GET_FINDING_LOCATIONS };
