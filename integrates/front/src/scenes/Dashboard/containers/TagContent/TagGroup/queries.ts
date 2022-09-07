/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const PORTFOLIO_GROUP_QUERY: DocumentNode = gql`
  query GetPortfoliosGroups($tag: String!) {
    tag(tag: $tag) {
      name
      groups {
        description
        name
      }
    }
  }
`;
