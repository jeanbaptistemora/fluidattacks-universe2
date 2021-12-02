import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_TOE_LINES: DocumentNode = gql`
  query GetToeLines(
    $groupName: String!
    $after: String
    $bePresent: Boolean
    $canGetAttackedAt: Boolean!
    $canGetAttackedLines: Boolean!
    $canGetBePresentUntil: Boolean!
    $canGetComments: Boolean!
    $first: Int
  ) {
    group(groupName: $groupName) {
      name
      toeLines(bePresent: $bePresent, after: $after, first: $first) {
        edges {
          node {
            attackedAt @include(if: $canGetAttackedAt)
            attackedLines @include(if: $canGetAttackedLines)
            bePresent
            bePresentUntil @include(if: $canGetBePresentUntil)
            comments @include(if: $canGetComments)
            commitAuthor
            filename
            loc
            modifiedCommit
            modifiedDate
            root {
              nickname
            }
            seenAt
            sortsRiskLevel
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
        __typename
      }
      __typename
    }
  }
`;

export { GET_TOE_LINES };
