/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const UPDATE_TOE_LINES_ATTACKED_LINES: DocumentNode = gql`
  mutation UpdateToeLinesAttackedLines(
    $groupName: String!
    $rootId: String!
    $filename: String!
    $comments: String!
    $attackedLines: Int
  ) {
    updateToeLinesAttackedLines(
      groupName: $groupName
      rootId: $rootId
      filename: $filename
      comments: $comments
      attackedLines: $attackedLines
    ) {
      success
    }
  }
`;

export { UPDATE_TOE_LINES_ATTACKED_LINES };
