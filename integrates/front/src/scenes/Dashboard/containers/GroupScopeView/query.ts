import type { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_ROOTS: DocumentNode = gql`
  query GetRoots($groupName: String!) {
    group: project(projectName: $groupName) {
      roots {
        ... on GitRoot {
          branch
          directoryFiltering {
            paths
            policy
          }
          environment {
            kind
            url
          }
          id
          url
        }
        ... on IPRoot {
          address
          id
          port
        }
        ... on URLRoot {
          host
          id
          path
          port
          protocol
        }
      }
    }
  }
`;
