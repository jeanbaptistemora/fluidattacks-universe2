/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";

const ADD_ENROLLMENT = gql`
  mutation AddEnrollmentMutation {
    addEnrollment {
      success
    }
  }
`;

const ADD_GIT_ROOT = gql`
  mutation AddGitRoot(
    $branch: String!
    $credentials: RootCredentialsInput
    $environment: String!
    $gitignore: [String!]!
    $groupName: String!
    $includesHealthCheck: Boolean!
    $nickname: String!
    $url: String!
    $useVpn: Boolean!
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
      useVpn: $useVpn
    ) {
      success
    }
  }
`;

const ADD_GROUP_MUTATION = gql`
  mutation AddGroupMutation(
    $description: String!
    $groupName: String!
    $hasMachine: Boolean!
    $hasSquad: Boolean!
    $language: Language!
    $organizationName: String!
    $service: ServiceType!
    $subscription: SubscriptionType!
  ) {
    addGroup(
      description: $description
      groupName: $groupName
      hasMachine: $hasMachine
      hasSquad: $hasSquad
      language: $language
      organizationName: $organizationName
      service: $service
      subscription: $subscription
    ) {
      success
    }
  }
`;

const ADD_ORGANIZATION = gql`
  mutation AddOrganization($name: String!) {
    addOrganization(name: $name) {
      organization {
        id
        name
      }
      success
    }
  }
`;

const GET_STAKEHOLDER_GROUPS = gql`
  query GetStakeholderGroups {
    me {
      organizations {
        groups {
          name
        }
        name
      }
      userEmail
    }
  }
`;

const VALIDATE_GIT_ACCESS = gql`
  mutation ValidateGitAccess(
    $branch: String!
    $credentials: RootCredentialsInput!
    $url: String!
  ) {
    validateGitAccess(branch: $branch, credentials: $credentials, url: $url) {
      success
    }
  }
`;

export {
  ADD_ENROLLMENT,
  ADD_GIT_ROOT,
  ADD_GROUP_MUTATION,
  ADD_ORGANIZATION,
  GET_STAKEHOLDER_GROUPS,
  VALIDATE_GIT_ACCESS,
};
