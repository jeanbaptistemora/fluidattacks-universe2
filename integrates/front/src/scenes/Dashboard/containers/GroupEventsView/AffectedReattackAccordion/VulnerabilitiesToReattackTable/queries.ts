/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FINDING_VULNS_TO_REATTACK: DocumentNode = gql`
  query GetFindingVulnsToReattack(
    $after: String
    $findingId: String!
    $first: Int
  ) {
    finding(identifier: $findingId) {
      __typename
      id
      vulnerabilitiesToReattackConnection(after: $after, first: $first) {
        edges {
          node {
            findingId
            id
            where
            specific
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
      }
    }
  }
`;

export { GET_FINDING_VULNS_TO_REATTACK };
