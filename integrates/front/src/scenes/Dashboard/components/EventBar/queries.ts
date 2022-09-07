/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ORG_EVENTS: DocumentNode = gql`
  query GetOrganizationEvents($organizationName: String!) {
    organizationId(organizationName: $organizationName) {
      groups {
        events {
          eventStatus
          eventDate
          groupName
        }
        name
      }
      name
    }
  }
`;

export { GET_ORG_EVENTS };
