import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_TOE_LINES: DocumentNode = gql`
  query GetToeLines($groupName: String!) {
    group: project(projectName: $groupName) {
      name
      roots {
        ... on GitRoot {
          id
          toeLines {
            filename
            modifiedDate
            modifiedCommit
            loc
            testedDate
            testedLines
            comments
          }
        }
      }
    }
  }
`;

export { GET_TOE_LINES };
