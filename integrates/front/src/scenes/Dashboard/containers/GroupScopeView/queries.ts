import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ROOTS: DocumentNode = gql`
  query GetRoots($groupName: String!) {
    group: project(projectName: $groupName) {
      name
      roots {
        ... on GitRoot {
          branch
          cloningStatus {
            message
            status
          }
          environment
          environmentUrls
          gitignore
          id
          includesHealthCheck
          lastStateStatusUpdate
          lastCloningStatusUpdate
          nickname
          state
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
    $gitignore: [String!]!
    $groupName: String!
    $includesHealthCheck: Boolean!
    $nickname: String!
    $url: String!
  ) {
    addGitRoot(
      branch: $branch
      environment: $environment
      gitignore: $gitignore
      groupName: $groupName
      includesHealthCheck: $includesHealthCheck
      nickname: $nickname
      url: $url
    ) {
      success
    }
  }
`;

const UPDATE_GIT_ENVIRONMENTS: DocumentNode = gql`
  mutation UpdateGitEnvironments(
    $groupName: String!
    $id: ID!
    $environmentUrls: [String!]!
  ) {
    updateGitEnvironments(
      groupName: $groupName
      id: $id
      environmentUrls: $environmentUrls
    ) {
      success
    }
  }
`;

const UPDATE_GIT_ROOT: DocumentNode = gql`
  mutation UpdateGitRoot(
    $environment: String!
    $gitignore: [String!]!
    $groupName: String!
    $id: ID!
    $includesHealthCheck: Boolean!
    $nickname: String!
  ) {
    updateGitRoot(
      environment: $environment
      gitignore: $gitignore
      groupName: $groupName
      id: $id
      includesHealthCheck: $includesHealthCheck
      nickname: $nickname
    ) {
      success
    }
  }
`;

const UPDATE_ROOT_STATE: DocumentNode = gql`
  mutation UpdateRootState(
    $groupName: String!
    $id: ID!
    $state: ResourceState!
  ) {
    updateRootState(groupName: $groupName, id: $id, state: $state) {
      success
    }
  }
`;

const ACTIVATE_ROOT: DocumentNode = gql`
  mutation ActivateRoot($groupName: String!, $id: ID!) {
    activateRoot(groupName: $groupName, id: $id) {
      success
    }
  }
`;

const DEACTIVATE_ROOT: DocumentNode = gql`
  mutation DeactivateRoot(
    $groupName: String!
    $id: ID!
    $reason: RootDeactivationReason!
  ) {
    deactivateRoot(groupName: $groupName, id: $id, reason: $reason) {
      success
    }
  }
`;

export {
  ACTIVATE_ROOT,
  ADD_GIT_ROOT,
  DEACTIVATE_ROOT,
  GET_ROOTS,
  UPDATE_GIT_ENVIRONMENTS,
  UPDATE_GIT_ROOT,
  UPDATE_ROOT_STATE,
};
