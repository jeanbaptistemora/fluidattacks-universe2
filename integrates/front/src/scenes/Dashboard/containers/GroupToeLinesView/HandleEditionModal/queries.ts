import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const UPDATE_TOE_LINES_ATTACKED_LINES: DocumentNode = gql`
  mutation UpdateToeLinesAttackedLines(
    $groupName: String!
    $rootId: String!
    $filenames: [String!]!
    $attackedAt: DateTime!
    $comments: String!
    $attackedLines: Int
  ) {
    updateToeLinesAttackedLines(
      groupName: $groupName
      rootId: $rootId
      filenames: $filenames
      attackedAt: $attackedAt
      comments: $comments
      attackedLines: $attackedLines
    ) {
      success
    }
  }
`;

export { UPDATE_TOE_LINES_ATTACKED_LINES };
