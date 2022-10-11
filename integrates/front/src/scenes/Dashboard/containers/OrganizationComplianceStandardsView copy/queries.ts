/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ORGANIZATION_GROUP_NAME: DocumentNode = gql`
  query GetOrganizationGroupNames($organizationId: String!) {
    organization(organizationId: $organizationId) {
      name
      groups {
        name
      }
    }
  }
`;

const GET_GROUP_UNFULFILLED_STANDARDS: DocumentNode = gql`
  query GetGroupUnfulfilledStandards($groupName: String!) {
    group(groupName: $groupName) {
      name
      compliance {
        unfulfilledStandards {
          title
          unfulfilledRequirements {
            id
            title
          }
        }
      }
    }
  }
`;

export { GET_ORGANIZATION_GROUP_NAME, GET_GROUP_UNFULFILLED_STANDARDS };
