import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const TOE_PORT_FRAGMENT: DocumentNode = gql`
  fragment toePortFields on ToePort {
    __typename
    address
    attackedAt @include(if: $canGetAttackedAt)
    attackedBy @include(if: $canGetAttackedBy)
    bePresent
    bePresentUntil @include(if: $canGetBePresentUntil)
    firstAttackAt @include(if: $canGetFirstAttackAt)
    hasVulnerabilities
    port
    root {
      __typename
      id
      nickname
    }
    seenAt
    seenFirstTimeBy @include(if: $canGetSeenFirstTimeBy)
  }
`;

const GET_TOE_PORTS: DocumentNode = gql`
  query GetToePorts(
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
      toePorts(
        bePresent: $bePresent
        after: $after
        first: $first
        rootId: $rootId
      ) {
        edges {
          node {
            ...toePortFields
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
  ${TOE_PORT_FRAGMENT}
`;

const UPDATE_TOE_PORT: DocumentNode = gql`
  mutation UpdateToePort(
    $address: String!
    $bePresent: Boolean!
    $canGetAttackedAt: Boolean!
    $canGetAttackedBy: Boolean!
    $canGetBePresentUntil: Boolean!
    $canGetFirstAttackAt: Boolean!
    $canGetSeenFirstTimeBy: Boolean!
    $groupName: String!
    $hasRecentAttack: Boolean
    $port: Int!
    $rootId: String!
    $shouldGetNewToePort: Boolean!
  ) {
    updateToePort(
      address: $address
      bePresent: $bePresent
      groupName: $groupName
      hasRecentAttack: $hasRecentAttack
      port: $port
      rootId: $rootId
    ) {
      success
      toePort @include(if: $shouldGetNewToePort) {
        ...toePortFields
      }
    }
  }
  ${TOE_PORT_FRAGMENT}
`;

export { GET_TOE_PORTS, UPDATE_TOE_PORT };
