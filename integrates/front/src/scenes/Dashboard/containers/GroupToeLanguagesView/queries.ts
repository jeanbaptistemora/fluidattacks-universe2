/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_TOE_LANGUAGES: DocumentNode = gql`
  query GetToeLanguages($groupName: String!) {
    group(groupName: $groupName) {
      name
      codeLanguages {
        language
        loc
      }
    }
  }
`;

export { GET_TOE_LANGUAGES };
