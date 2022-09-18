/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */
import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_GROUP_SERVICES = gql`
  query GetGroupServices($groupName: String!) {
    group(groupName: $groupName) {
      name
      serviceAttributes
    }
  }
`;

const GET_ME_VULNERABILITIES_ASSIGNED_IDS: DocumentNode = gql`
  query GetMeVulnerabilitiesAssignedIds {
    me(callerOrigin: "FRONT") {
      vulnerabilitiesAssigned {
        id
      }
      userEmail
    }
  }
`;

const REQUEST_GROUPS_UPGRADE_MUTATION: DocumentNode = gql`
  mutation RequestGroupsUpgrade($groupNames: [String!]!) {
    requestGroupsUpgrade(groupNames: $groupNames) {
      success
    }
  }
`;

export {
  GET_GROUP_SERVICES,
  GET_ME_VULNERABILITIES_ASSIGNED_IDS,
  REQUEST_GROUPS_UPGRADE_MUTATION,
};
