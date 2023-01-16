import { gql } from "@apollo/client";

const ADD_ENROLLMENT = gql`
  mutation AddEnrollment {
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

const ADD_GROUP = gql`
  mutation AddGroup(
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
  mutation AddOrganization($country: String!, $name: String!) {
    addOrganization(country: $country, name: $name) {
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
      company {
        trial {
          completed
          startDate
        }
      }
      organizations {
        country
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
  ADD_GROUP,
  ADD_ORGANIZATION,
  GET_STAKEHOLDER_GROUPS,
  VALIDATE_GIT_ACCESS,
};
