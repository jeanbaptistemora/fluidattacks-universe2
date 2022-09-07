/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_FORCES_TOKEN: DocumentNode = gql`
  query GetForcesToken($groupName: String!) {
    group(groupName: $groupName) {
      forcesToken
      name
    }
  }
`;

const UPDATE_FORCES_TOKEN_MUTATION: DocumentNode = gql`
  mutation UpdateForcesAccessTokenMutation($groupName: String!) {
    updateForcesAccessToken(groupName: $groupName) {
      success
      sessionJwt
    }
  }
`;

export { GET_FORCES_TOKEN, UPDATE_FORCES_TOKEN_MUTATION };
