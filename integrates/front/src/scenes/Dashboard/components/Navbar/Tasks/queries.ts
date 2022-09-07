/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ME_VULNERABILITIES_ASSIGNED_IDS: DocumentNode = gql`
  query GetMeVulnerabilitiesAssignedIds {
    me(callerOrigin: "FRONT") {
      vulnerabilitiesAssigned {
        id
      }
      userEmail
    }
  }
`;

export { GET_ME_VULNERABILITIES_ASSIGNED_IDS };
