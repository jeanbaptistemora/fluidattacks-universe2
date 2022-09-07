/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ADD_GROUP_MUTATION: DocumentNode = gql`
  mutation AddGroupMutation(
    $description: String!
    $groupName: String!
    $hasMachine: Boolean!
    $hasSquad: Boolean!
    $language: Language!
    $organizationName: String!
    $service: ServiceType!
    $subscription: SubscriptionType!
  ) {
    addGroup(
      description: $description
      groupName: $groupName
      hasMachine: $hasMachine
      hasSquad: $hasSquad
      language: $language
      organizationName: $organizationName
      service: $service
      subscription: $subscription
    ) {
      success
    }
  }
`;

export { ADD_GROUP_MUTATION };
