import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_TOE_LINES: DocumentNode = gql`
  query GetToeLines(
    $groupName: String!
    $after: String
    $bePresent: Boolean
    $canGetAttackedAt: Boolean!
    $canGetAttackedBy: Boolean!
    $canGetAttackedLines: Boolean!
    $canGetBePresentUntil: Boolean!
    $canGetComments: Boolean!
    $canGetFirstAttackAt: Boolean!
    $first: Int
    $rootId: ID
  ) {
    group(groupName: $groupName) {
      name
      toeLines(
        bePresent: $bePresent
        after: $after
        first: $first
        rootId: $rootId
      ) {
        edges {
          node {
            attackedAt @include(if: $canGetAttackedAt)
            attackedBy @include(if: $canGetAttackedBy)
            attackedLines @include(if: $canGetAttackedLines)
            bePresent
            bePresentUntil @include(if: $canGetBePresentUntil)
            comments @include(if: $canGetComments)
            filename
            firstAttackAt @include(if: $canGetFirstAttackAt)
            hasVulnerabilities
            lastAuthor
            lastCommit
            loc
            modifiedDate
            root {
              id
              nickname
            }
            seenAt
            sortsRiskLevel
            sortsSuggestions {
              findingTitle
              probability
            }
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
