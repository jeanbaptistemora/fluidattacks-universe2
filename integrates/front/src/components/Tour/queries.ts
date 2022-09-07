/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const UPDATE_TOURS: DocumentNode = gql`
  mutation updateTours($newGroup: Boolean!, $newRoot: Boolean!) {
    updateTours(tours: { newGroup: $newGroup, newRoot: $newRoot }) {
      success
    }
  }
`;

export { UPDATE_TOURS };
