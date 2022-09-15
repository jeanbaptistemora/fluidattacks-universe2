/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_GROUP_VULNERABILITIES: DocumentNode = gql`
  query GetFindingVulnerabilities(
    $after: String
    $first: Int
    $groupName: String!
    $search: String
    $treatment: String
    $stateStatus: String
    $verificationStatus: String
  ) {
    group(groupName: $groupName) {
      name
      vulnerabilities(
        after: $after
        first: $first
        search: $search
        treatment: $treatment
        stateStatus: $stateStatus
        verificationStatus: $verificationStatus
      ) {
        edges {
          node {
            currentState
            finding {
              id
              severityScore
              title
            }
            id
            reportDate
            specific
            treatment
            verification
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

export { GET_GROUP_VULNERABILITIES };
