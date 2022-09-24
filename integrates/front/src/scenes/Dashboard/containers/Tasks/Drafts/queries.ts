/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_TODO_DRAFTS: DocumentNode = gql`
  query GetTodoDrafts {
    me {
      drafts {
        currentState
        groupName
        id
        openVulnerabilities
        reportDate
        severityScore
        title
      }
      userEmail
    }
  }
`;
