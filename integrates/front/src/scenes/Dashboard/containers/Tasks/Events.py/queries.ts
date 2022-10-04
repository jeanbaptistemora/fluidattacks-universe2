/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_TODO_EVENTS: DocumentNode = gql`
  query GetTodoEvents {
    me {
      userEmail
      pendingEvents {
        eventDate
        detail
        id
        groupName
        eventStatus
        eventType
        root {
          ... on GitRoot {
            id
            nickname
          }

          ... on URLRoot {
            id
            nickname
          }
          ... on IPRoot {
            id
            nickname
          }
        }
      }
    }
  }
`;
