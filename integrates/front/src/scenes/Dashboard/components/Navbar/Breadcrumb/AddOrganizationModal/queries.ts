/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ADD_NEW_ORGANIZATION: DocumentNode = gql`
  mutation AddOrganization($country: String!, $name: String!) {
    addOrganization(country: $country, name: $name) {
      organization {
        id
        name
      }
      success
    }
  }
`;

export { ADD_NEW_ORGANIZATION };
