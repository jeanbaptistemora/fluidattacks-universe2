/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_GROUP_VULNS: DocumentNode = gql`
  query GetGroupVulns($org: String!) {
    organizationId(organizationName: $org) {
      name
      groups {
        name
      }
    }
  }
`;
