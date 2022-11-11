/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_ORGANIZATION_GROUPS: DocumentNode = gql`
  query GetOrganizationGroups($organizationId: String!) {
    organization(organizationId: $organizationId) {
      name
      groups {
        name
        description
        hasMachine
        hasSquad
        openFindings
        service
        subscription
        userRole
        events {
          eventStatus
        }
        managed
      }
    }
  }
`;
