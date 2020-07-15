import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_ORGANIZATION_USERS: DocumentNode = gql`
  query GetOrganizationUsers ($organizationId: String!) {
    organization(organizationId: $organizationId) {
      users {
        email
        firstLogin
        lastLogin
        phoneNumber
        role
      }
    }
  }
  `;

export const ADD_USER_MUTATION: DocumentNode = gql`
  mutation GrantUserOrganizationAccessMutation(
    $email: String!,
    $organizationId: String!,
    $phoneNumber: String,
    $role: OrganizationRole!
    ) {
    grantUserOrganizationAccess (
      organizationId: $organizationId,
      phoneNumber: $phoneNumber,
      role: $role,
      userEmail: $email,
    ) {
      success
      grantedUser {
        email
      }
    }
  }
  `;

export const EDIT_USER_MUTATION: DocumentNode = gql`
  mutation EditUserOrganizationMutation(
    $email: String!,
    $organizationId: String!,
    $phoneNumber: String,
    $role: OrganizationRole!
  ) {
    editUserOrganization (
      organizationId: $organizationId,
      phoneNumber: $phoneNumber,
      role: $role
      userEmail: $email
    ) {
      success
      modifiedUser {
        email
      }
    }
  }
  `;

export const REMOVE_USER_MUTATION: DocumentNode = gql`
  mutation RemoveUserOrganizationAccessMutation(
    $organizationId: String!,
    $userEmail: String!,
    ) {
      removeUserOrganizationAccess (
        organizationId: $organizationId,
        userEmail: $userEmail
      ) {
        success
      }
    }
  `;
