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
    $after: String
    $attackedBy: String
    $bePresent: Boolean
    $canGetAttackedAt: Boolean!
    $canGetAttackedBy: Boolean!
    $canGetAttackedLines: Boolean!
    $canGetBePresentUntil: Boolean!
    $canGetComments: Boolean!
    $canGetFirstAttackAt: Boolean!
    $comments: String
    $filename: String
    $first: Int
    $fromAttackedAt: DateTime
    $fromBePresentUntil: DateTime
    $fromFirstAttackAt: DateTime
    $fromModifiedDate: DateTime
    $fromSeenAt: DateTime
    $groupName: String!
    $hasVulnerabilities: Boolean
    $lastAuthor: String
    $lastCommit: String
    $maxAttackedLines: Int
    $maxLoc: Int
    $maxSortsRiskLevel: Int
    $minAttackedLines: Int
    $minLoc: Int
    $minSortsRiskLevel: Int
    $rootId: ID
    $toAttackedAt: DateTime
    $toBePresentUntil: DateTime
    $toFirstAttackAt: DateTime
    $toModifiedDate: DateTime
    $toSeenAt: DateTime
  ) {
    group(groupName: $groupName) {
      name
      toeLines(
        after: $after
        attackedBy: $attackedBy
        bePresent: $bePresent
        comments: $comments
        filename: $filename
        first: $first
        fromAttackedAt: $fromAttackedAt
        fromBePresentUntil: $fromBePresentUntil
        fromFirstAttackAt: $fromFirstAttackAt
        fromModifiedDate: $fromModifiedDate
        fromSeenAt: $fromSeenAt
        hasVulnerabilities: $hasVulnerabilities
        lastAuthor: $lastAuthor
        lastCommit: $lastCommit
        maxAttackedLines: $maxAttackedLines
        maxLoc: $maxLoc
        maxSortsRiskLevel: $maxSortsRiskLevel
        minAttackedLines: $minAttackedLines
        minLoc: $minLoc
        minSortsRiskLevel: $minSortsRiskLevel
        rootId: $rootId
        toAttackedAt: $toAttackedAt
        toBePresentUntil: $toBePresentUntil
        toFirstAttackAt: $toFirstAttackAt
        toModifiedDate: $toModifiedDate
        toSeenAt: $toSeenAt
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
        total
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
