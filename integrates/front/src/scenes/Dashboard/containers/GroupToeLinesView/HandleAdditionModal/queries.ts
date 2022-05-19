import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

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

export { GET_GIT_ROOTS };
