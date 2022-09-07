/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_BILLING: DocumentNode = gql`
  query GetBilling($date: DateTime, $groupName: String!) {
    group(groupName: $groupName) {
      authors(date: $date) {
        data {
          actor
          commit
          groups
          organization
          repository
        }
      }
      name
    }
  }
`;
