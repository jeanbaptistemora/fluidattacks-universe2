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
          credentials {
            id
            name
            type
          }
          environment
          environmentUrls
          gitignore
          id
          includesHealthCheck
          nickname
          state
          url
        }
        ... on IPRoot {
          address
          id
          nickname
          port
          state
        }
        ... on URLRoot {
          host
          id
          nickname
          path
          port
          protocol
          state
        }
      }
    }
  }
`;

const GET_GIT_ROOT_DETAILS = gql`
  query GetGitRootDetails($groupName: String!, $rootId: ID!) {
    root(groupName: $groupName, rootId: $rootId) {
      ... on GitRoot {
        cloningStatus {
          message
        }
        environment
        environmentUrls
        gitignore
        id
        lastCloningStatusUpdate
        lastMachineExecutions {
          complete {
            stoppedAt
          }
          specific {
            findingsExecuted {
              finding
            }
            stoppedAt
          }
        }
        lastStateStatusUpdate
        nickname
      }
    }
  }
`;

const ADD_GIT_ROOT: DocumentNode = gql`
  mutation AddGitRoot(
    $branch: String!
    $credentials: CredentialsInput
    $environment: String!
    $gitignore: [String!]!
    $groupName: String!
    $includesHealthCheck: Boolean!
    $nickname: String!
    $url: String!
  ) {
    addGitRoot(
      branch: $branch
      credentials: $credentials
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
    $branch: String!
    $credentials: CredentialsInput
    $environment: String!
    $gitignore: [String!]!
    $groupName: String!
    $id: ID!
    $includesHealthCheck: Boolean!
    $url: String!
  ) {
    updateGitRoot(
      branch: $branch
      credentials: $credentials
      environment: $environment
      gitignore: $gitignore
      groupName: $groupName
      id: $id
      includesHealthCheck: $includesHealthCheck
      url: $url
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
  mutation AddUrlRoot($url: String!, $groupName: String!, $nickname: String!) {
    addUrlRoot(url: $url, groupName: $groupName, nickname: $nickname) {
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

const MOVE_ROOT: DocumentNode = gql`
  mutation MoveRoot($groupName: String!, $id: ID!, $targetGroupName: String!) {
    moveRoot(
      groupName: $groupName
      id: $id
      targetGroupName: $targetGroupName
    ) {
      success
    }
  }
`;

const GET_GROUPS: DocumentNode = gql`
  query GetGroups {
    me {
      organizations {
        groups {
          name
          organization
          service
        }
        name
      }
      userEmail
    }
  }
`;

const GET_ROOTS_VULNS: DocumentNode = gql`
  query GetRootsVulns($groupName: String!) {
    group(groupName: $groupName) {
      name
      roots {
        ... on GitRoot {
          id
          vulnerabilities {
            id
            vulnerabilityType
          }
        }
        ... on IPRoot {
          id
          vulnerabilities {
            id
            vulnerabilityType
          }
        }
        ... on URLRoot {
          id
          vulnerabilities {
            id
            vulnerabilityType
          }
        }
      }
    }
  }
`;

const SYNC_GIT_ROOT: DocumentNode = gql`
  mutation SyncGitRoot($groupName: String!, $rootId: String!) {
    syncGitRoot(groupName: $groupName, rootId: $rootId) {
      success
    }
  }
`;

const VALIDATE_GIT_ACCESS: DocumentNode = gql`
  mutation ValidateGitAccess(
    $credentials: CredentialsInput!
    $groupName: String!
    $url: String!
  ) {
    validateGitAccess(
      credentials: $credentials
      groupName: $groupName
      url: $url
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
  GET_GIT_ROOT_DETAILS,
  GET_GROUPS,
  GET_ROOTS_VULNS,
  GET_ROOTS,
  MOVE_ROOT,
  SYNC_GIT_ROOT,
  UPDATE_GIT_ENVIRONMENTS,
  UPDATE_GIT_ROOT,
  VALIDATE_GIT_ACCESS,
};
