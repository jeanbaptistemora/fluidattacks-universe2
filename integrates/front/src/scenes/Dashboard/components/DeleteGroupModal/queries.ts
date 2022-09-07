/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const REMOVE_GROUP_MUTATION: DocumentNode = gql`
  mutation RemoveGroupMutation(
    $groupName: String!
    $reason: RemoveGroupReason!
  ) {
    removeGroup(groupName: $groupName, reason: $reason) {
      success
    }
  }
`;

export { REMOVE_GROUP_MUTATION };
