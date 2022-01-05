import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_TOE_INPUTS: DocumentNode = gql`
  query GetToeInputs(
    $after: String
    $bePresent: Boolean
    $canGetAttackedAt: Boolean!
    $canGetAttackedBy: Boolean!
    $canGetBePresentUntil: Boolean!
    $canGetFirstAttackAt: Boolean!
    $canGetSeenFirstTimeBy: Boolean!
    $first: Int
    $groupName: String!
  ) {
    group(groupName: $groupName) {
      name
      toeInputs(bePresent: $bePresent, after: $after, first: $first) {
        edges {
          node {
            attackedAt @include(if: $canGetAttackedAt)
            attackedBy @include(if: $canGetAttackedBy)
            bePresent
            bePresentUntil @include(if: $canGetBePresentUntil)
            component
            entryPoint
            firstAttackAt @include(if: $canGetFirstAttackAt)
            seenAt
            seenFirstTimeBy @include(if: $canGetSeenFirstTimeBy)
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
