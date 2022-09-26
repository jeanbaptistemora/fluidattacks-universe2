/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ORGANIZATION_COMPLIANCE: DocumentNode = gql`
  query GetOrganizationCompliance($organizationId: String!) {
    organization(organizationId: $organizationId) {
      __typename
      name
      compliance {
        nonComplianceLevel
      }
    }
  }
`;

export { GET_ORGANIZATION_COMPLIANCE };
