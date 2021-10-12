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
  mutation AddStakeholderMutation($email: String!, $role: StakeholderRole!) {
    addStakeholder(email: $email, role: $role) {
      success
      email
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
      permissions
      remember
      role
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
  GET_ORG_LEVEL_PERMISSIONS,
  GET_GROUP_LEVEL_PERMISSIONS,
};
