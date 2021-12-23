import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_TOE_INPUTS: DocumentNode = gql`
  query GetToeInputs(
    $after: String
    $bePresent: Boolean
    $groupName: String!
    $first: Int
  ) {
    group(groupName: $groupName) {
      name
      toeInputs(bePresent: $bePresent, after: $after, first: $first) {
        edges {
          node {
            attackedAt
            attackedBy
            bePresent
            bePresentUntil
            component
            entryPoint
            firstAttackAt
            seenAt
            seenFirstTimeBy
            unreliableRootNickname
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
        __typename
      }
    }
  }
`;

export { GET_TOE_INPUTS };
