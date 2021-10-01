import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ROOTS: DocumentNode = gql`
  query GetRoots($groupName: String!) {
    group(groupName: $groupName) {
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
          state
        }
        ... on URLRoot {
          host
          id
          path
          port
          protocol
          state
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

const ADD_IP_ROOT = gql`
  mutation AddIpRoot(
    $address: String!
    $groupName: String!
    $nickname: String!
    $port: Int!
  ) {
    addIpRoot(
      address: $address
      groupName: $groupName
      nickname: $nickname
      port: $port
    ) {
      success
    }
  }
`;

const ADD_URL_ROOT = gql`
  mutation AddUrlRoot($url: String!, $groupName: String!) {
    addUrlRoot(url: $url, groupName: $groupName) {
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
    $other: String
    $reason: RootDeactivationReason!
  ) {
    deactivateRoot(
      groupName: $groupName
      id: $id
      other: $other
      reason: $reason
    ) {
      success
    }
  }
`;

export {
  ACTIVATE_ROOT,
  ADD_GIT_ROOT,
  ADD_IP_ROOT,
  ADD_URL_ROOT,
  DEACTIVATE_ROOT,
  GET_ROOTS,
  UPDATE_GIT_ENVIRONMENTS,
  UPDATE_GIT_ROOT,
};
