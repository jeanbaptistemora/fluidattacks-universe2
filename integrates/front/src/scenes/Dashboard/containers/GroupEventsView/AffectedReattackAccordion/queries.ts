/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_VERIFIED_FINDING_INFO: DocumentNode = gql`
  query GetVerifiedFindingInfo($groupName: String!) {
    group(groupName: $groupName) {
      findings {
        id
        title
        verified
      }
      name
    }
  }
`;

export { GET_VERIFIED_FINDING_INFO };
