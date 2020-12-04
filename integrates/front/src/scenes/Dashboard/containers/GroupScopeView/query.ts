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
          includesHealthCheck
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

const UPDATE_GIT_ROOT: DocumentNode = gql`
  mutation UpdateGitRoot(
    $environment: String!
    $filter: GitRootFilterInput
    $id: ID!
    $includesHealthCheck: Boolean!
  ) {
    updateGitRoot(
      environment: $environment
      filter: $filter
      id: $id
      includesHealthCheck: $includesHealthCheck
    ) {
      success
    }
  }
`;

const UPDATE_ROOT_STATE: DocumentNode = gql`
  mutation UpdateRootState($id: ID!, $state: ResourceState!) {
    updateRootState(id: $id, state: $state) {
      success
    }
  }
`;

export { GET_ROOTS, ADD_GIT_ROOT, UPDATE_GIT_ROOT, UPDATE_ROOT_STATE };
