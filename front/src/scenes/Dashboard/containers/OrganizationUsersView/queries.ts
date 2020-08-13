import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_ORGANIZATION_STAKEHOLDERS: DocumentNode = gql`
  query GetOrganizationStakeholders ($organizationId: String!) {
    organization(organizationId: $organizationId) {
      stakeholders {
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

export const EDIT_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation EditStakeholderOrganizationMutation(
    $email: String!,
    $organizationId: String!,
    $phoneNumber: String,
    $role: OrganizationRole!
  ) {
    editStakeholderOrganization (
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
