import type { DocumentNode } from "graphql";
import gql from "graphql-tag";

const GET_ROOTS: DocumentNode = gql`
  query GetRoots($groupName: String!) {
    group: project(projectName: $groupName) {
      roots {
        ... on GitRoot {
          branch
          environment
          filter {
            paths
            policy
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

const ADD_GIT_ROOT: DocumentNode = gql`
  mutation AddGitRoot(
    $branch: String!
    $environment: String!
    $filter: GitRootFilterInput
    $groupName: String!
    $includesHealthCheck: Boolean!
    $url: String!
  ) {
    addGitRoot(
      branch: $branch
      environment: $environment
      filter: $filter
      groupName: $groupName
      includesHealthCheck: $includesHealthCheck
      url: $url
    ) {
      success
    }
  }
`;

export { GET_ROOTS, ADD_GIT_ROOT };
