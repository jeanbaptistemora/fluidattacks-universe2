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
