/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_STAKEHOLDER: DocumentNode = gql`
  query GetStakeholderDataQuery(
    $entity: StakeholderEntity!
    $organizationId: String
    $groupName: String
    $userEmail: String!
  ) {
    stakeholder(
      entity: $entity
      organizationId: $organizationId
      groupName: $groupName
      userEmail: $userEmail
    ) {
      email
      responsibility
    }
  }
`;
