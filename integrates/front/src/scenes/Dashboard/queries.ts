import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ACCEPT_LEGAL_MUTATION: DocumentNode = gql`
  mutation AcceptLegalMutation($remember: Boolean!) {
    acceptLegal(remember: $remember) {
      success
    }
  }
`;

const ACKNOWLEDGE_CONCURRENT_SESSION: DocumentNode = gql`
  mutation AcknowledgeConcurrentSessionMutation {
    acknowledgeConcurrentSession {
      success
    }
  }
`;

const ADD_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation AddStakeholderMutation(
    $email: String!
    $role: StakeholderRole!
    $phoneNumber: String
  ) {
    addStakeholder(email: $email, role: $role, phoneNumber: $phoneNumber) {
      success
      email
    }
  }
`;

const GET_USER_PERMISSIONS: DocumentNode = gql`
  query GetPermissions($entity: Entity!, $identifier: String) {
    me(callerOrigin: "FRONT") {
      permissions(entity: $entity, identifier: $identifier)
      role(entity: $entity, identifier: $identifier)
      userEmail
    }
  }
`;

const GET_ORG_LEVEL_PERMISSIONS: DocumentNode = gql`
  query GetOrgLevelPermissions($identifier: String!) {
    organization(organizationId: $identifier) {
      name
      permissions(identifier: $identifier)
      userRole(identifier: $identifier)
    }
  }
`;

const GET_GROUP_LEVEL_PERMISSIONS: DocumentNode = gql`
  query GetGroupLevelPermissions($identifier: String!) {
    group(groupName: $identifier) {
      name
      permissions
      userRole
    }
  }
`;

const GET_USER: DocumentNode = gql`
  query GetUser {
    me(callerOrigin: "FRONT") {
      isConcurrentSession
      permissions(entity: USER)
      remember
      role(entity: USER)
      sessionExpiration
      userEmail
      userName
    }
  }
`;

export {
  ACCEPT_LEGAL_MUTATION,
  ACKNOWLEDGE_CONCURRENT_SESSION,
  ADD_STAKEHOLDER_MUTATION,
  GET_USER,
  GET_USER_PERMISSIONS,
  GET_ORG_LEVEL_PERMISSIONS,
  GET_GROUP_LEVEL_PERMISSIONS,
};
