/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";

const GET_GROUP_SERVICES = gql`
  query GetGroupServices($groupName: String!) {
    group(groupName: $groupName) {
      name
      serviceAttributes
    }
  }
`;

export { GET_GROUP_SERVICES };
