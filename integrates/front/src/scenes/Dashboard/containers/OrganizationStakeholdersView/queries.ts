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

export const ADD_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation GrantStakeholderOrganizationAccessMutation(
    $email: String!,
    $organizationId: String!,
    $phoneNumber: String,
    $role: OrganizationRole!
    ) {
    grantStakeholderOrganizationAccess (
      organizationId: $organizationId,
      phoneNumber: $phoneNumber,
      role: $role,
      userEmail: $email,
    ) {
      success
      grantedStakeholder {
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
      modifiedStakeholder {
        email
      }
    }
  }
  `;

export const REMOVE_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation RemoveStakeholderOrganizationAccessMutation(
    $organizationId: String!,
    $userEmail: String!,
    ) {
      removeStakeholderOrganizationAccess (
        organizationId: $organizationId,
        userEmail: $userEmail
      ) {
        success
      }
    }
  `;
