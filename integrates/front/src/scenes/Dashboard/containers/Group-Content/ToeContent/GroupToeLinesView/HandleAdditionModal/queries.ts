import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ADD_TOE_LINES: DocumentNode = gql`
  mutation AddToeLines(
    $filename: String!
    $groupName: String!
    $lastAuthor: String!
    $lastCommit: String!
    $loc: Int!
    $modifiedDate: DateTime!
    $rootId: String!
  ) {
    addToeLines(
      filename: $filename
      groupName: $groupName
      lastAuthor: $lastAuthor
      lastCommit: $lastCommit
      loc: $loc
      modifiedDate: $modifiedDate
      rootId: $rootId
    ) {
      success
    }
  }
`;

const GET_GIT_ROOTS: DocumentNode = gql`
  query GetGitRootsInfo($groupName: String!) {
    group(groupName: $groupName) {
      name
      roots {
        ... on GitRoot {
          __typename
          id
          nickname
          state
        }
      }
    }
  }
`;

export { ADD_TOE_LINES, GET_GIT_ROOTS };
