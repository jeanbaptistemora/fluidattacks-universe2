import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_ORGANIZATION_USERS: DocumentNode = gql`
  query GetOrganizationUsers ($organizationId: String!) {
    organization(organizationId: $organizationId) {
      users {
        email
        phoneNumber
        organization
        firstLogin
        lastLogin
      }
    }
  }
  `;

export const ADD_USER_MUTATION: DocumentNode = gql`
  mutation GrantUserOrganizationAccessMutation(
    $email: String!,
    $organization: String!,
    $organizationId: String!,
    $phoneNumber: String,
    $role: OrganizationRole!
    ) {
    grantUserOrganizationAccess (
      organizationId: $organizationId,
      phoneNumber: $phoneNumber,
      role: $role,
      userEmail: $email,
      userOrganization: $organization
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
    $organization: String!,
    $organizationId: String!,
    $phoneNumber: String,
    $role: OrganizationRole!
  ) {
    editUserOrganization (
      organization: $organization,
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
