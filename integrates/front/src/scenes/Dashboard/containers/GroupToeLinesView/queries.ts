import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_TOE_LINES: DocumentNode = gql`
  query GetToeLines($groupName: String!) {
    group(groupName: $groupName) {
      name
      roots {
        ... on GitRoot {
          id
          nickname
          toeLines {
            filename
            modifiedDate
            modifiedCommit
            loc
            testedDate
            testedLines
            comments
            sortsRiskLevel
          }
        }
      }
    }
  }
`;

export { GET_TOE_LINES };
