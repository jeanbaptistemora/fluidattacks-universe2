import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_TOE_INPUTS: DocumentNode = gql`
  query GetToeInputs($groupName: String!) {
    group(groupName: $groupName) {
      name
      toeInputs {
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
