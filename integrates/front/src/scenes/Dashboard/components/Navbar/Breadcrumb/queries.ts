/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FINDING_TITLE: DocumentNode = gql`
  query GetFindingTitle($findingId: String!) {
    finding(identifier: $findingId) {
      id
      title
    }
  }
`;

const GET_ORGANIZATION_GROUP_NAMES: DocumentNode = gql`
  query GetOrganizationGroupNames($organizationId: String!) {
    organization(organizationId: $organizationId) {
      name
      groups {
        name
      }
    }
  }
`;

const GET_USER_ORGANIZATIONS: DocumentNode = gql`
  query GetUserOrganizations {
    me(callerOrigin: "FRONT") {
      organizations {
        name
      }
      userEmail
    }
  }
`;

const GET_USER_TAGS: DocumentNode = gql`
  query GetUserTags($organizationId: String!) {
    me(callerOrigin: "FRONT") {
      tags(organizationId: $organizationId) {
        name
      }
      userEmail
    }
  }
`;

export {
  GET_FINDING_TITLE,
  GET_ORGANIZATION_GROUP_NAMES,
  GET_USER_ORGANIZATIONS,
  GET_USER_TAGS,
};
