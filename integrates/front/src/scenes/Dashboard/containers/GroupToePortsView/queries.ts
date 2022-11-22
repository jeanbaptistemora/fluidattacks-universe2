/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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

export { GET_TOE_PORTS };
