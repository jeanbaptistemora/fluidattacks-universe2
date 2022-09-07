/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FINDING_LOCATIONS: DocumentNode = gql`
  query GetFindingLocations($after: String, $findingId: String!, $first: Int) {
    finding(identifier: $findingId) {
      __typename
      id
      vulnerabilitiesConnection(after: $after, first: $first) {
        edges {
          node {
            currentState
            id
            treatmentAssigned
            where
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

export { GET_FINDING_LOCATIONS };
