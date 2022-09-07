/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const UNSUBSCRIBE_FROM_GROUP_MUTATION: DocumentNode = gql`
  mutation UnsubscribeFromGroupMutation($groupName: String!) {
    unsubscribeFromGroup(groupName: $groupName) {
      success
    }
  }
`;

export { UNSUBSCRIBE_FROM_GROUP_MUTATION };
