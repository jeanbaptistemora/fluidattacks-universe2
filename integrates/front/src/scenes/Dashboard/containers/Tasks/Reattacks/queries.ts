/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_TODO_REATTACKS: DocumentNode = gql`
  query GetTodoReattacks {
    me {
      userEmail
      organizations {
        name
        groups {
          name
          vulnerabilities(
            stateStatus: "OPEN"
            verificationStatus: "REQUESTED"
            first: 25
          ) {
            edges {
              node {
                lastRequestedReattackDate
                groupName
                id
                verification
                finding {
                  id
                  severityScore
                  title
                }
              }
            }
          }
        }
      }
    }
  }
`;
