import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const TOE_LINES_FRAGMENT: DocumentNode = gql`
  fragment toeLinesFields on ToeLines {
    __typename
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
`;

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
            ...toeLinesFields
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
  ${TOE_LINES_FRAGMENT}
`;

const VERIFY_TOE_LINES: DocumentNode = gql`
  mutation VerifyToeLines(
    $groupName: String!
    $rootId: String!
    $filename: String!
    $attackedLines: Int
    $canGetAttackedAt: Boolean!
    $canGetAttackedBy: Boolean!
    $canGetAttackedLines: Boolean!
    $canGetBePresentUntil: Boolean!
    $canGetComments: Boolean!
    $canGetFirstAttackAt: Boolean!
    $shouldGetNewToeLines: Boolean!
  ) {
    updateToeLinesAttackedLines(
      attackedLines: $attackedLines
      groupName: $groupName
      rootId: $rootId
      filename: $filename
      comments: ""
    ) {
      success
      toeLines @include(if: $shouldGetNewToeLines) {
        ...toeLinesFields
      }
    }
  }
  ${TOE_LINES_FRAGMENT}
`;

export { GET_TOE_LINES, VERIFY_TOE_LINES };
