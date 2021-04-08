import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_TOE_LINES: DocumentNode = gql`
  query GetRoots($groupName: String!) {
    group: project(projectName: $groupName) {
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
