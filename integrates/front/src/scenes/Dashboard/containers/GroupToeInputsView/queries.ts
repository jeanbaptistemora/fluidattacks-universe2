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
    $rootId: ID
  ) {
    group(groupName: $groupName) {
      name
      toeInputs(
        bePresent: $bePresent
        after: $after
        first: $first
        rootId: $rootId
      ) {
        edges {
          node {
            attackedAt @include(if: $canGetAttackedAt)
            attackedBy @include(if: $canGetAttackedBy)
            bePresent
            bePresentUntil @include(if: $canGetBePresentUntil)
            component
            entryPoint
            firstAttackAt @include(if: $canGetFirstAttackAt)
            hasVulnerabilities
            seenAt
            seenFirstTimeBy @include(if: $canGetSeenFirstTimeBy)
            root {
              ... on GitRoot {
                __typename
                id
                nickname
              }
              ... on IPRoot {
                __typename
                id
                nickname
              }
              ... on URLRoot {
                __typename
                id
                nickname
              }
            }
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

const UPDATE_TOE_INPUT: DocumentNode = gql`
  mutation UpdateToeInput(
    $bePresent: Boolean!
    $component: String!
    $entryPoint: String!
    $groupName: String!
    $hasRecentAttack: Boolean
    $rootId: String!
  ) {
    updateToeInput(
      bePresent: $bePresent
      component: $component
      entryPoint: $entryPoint
      groupName: $groupName
      hasRecentAttack: $hasRecentAttack
      rootId: $rootId
    ) {
      success
    }
  }
`;

export { GET_TOE_INPUTS, UPDATE_TOE_INPUT };
