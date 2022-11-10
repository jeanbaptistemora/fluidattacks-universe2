/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ORGANIZATION_INTEGRATION_REPOSITORIES: DocumentNode = gql`
  query GetOrganizationIntegrationRepositories($organizationId: String!) {
    organization(organizationId: $organizationId) {
      __typename
      name
      integrationRepositories {
        __typename
        defaultBranch
        lastCommitDate
        url
      }
    }
  }
`;

const GET_ORGANIZATION_GROUPS: DocumentNode = gql`
  query GeOrganizationGroups($organizationId: String!) {
    organization(organizationId: $organizationId) {
      __typename
      groups {
        name
        permissions
        serviceAttributes
      }
      name
      permissions
    }
  }
`;

export { GET_ORGANIZATION_INTEGRATION_REPOSITORIES, GET_ORGANIZATION_GROUPS };
