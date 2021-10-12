import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ORGANIZATION_STAKEHOLDERS: DocumentNode = gql`
  query GetOrganizationStakeholders($organizationId: String!) {
    organization(organizationId: $organizationId) {
      name
      stakeholders {
        email
        firstLogin
        lastLogin
        role
      }
    }
  }
`;

const ADD_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation GrantStakeholderOrganizationAccessMutation(
    $email: String!
    $organizationId: String!
    $role: OrganizationRole!
  ) {
    grantStakeholderOrganizationAccess(
      organizationId: $organizationId
      role: $role
      userEmail: $email
    ) {
      success
      grantedStakeholder {
        email
      }
    }
  }
`;

const UPDATE_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation UpdateOrganizationStakeholderMutation(
    $email: String!
    $organizationId: String!
    $role: OrganizationRole!
  ) {
    updateOrganizationStakeholder(
      organizationId: $organizationId
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

const REMOVE_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation RemoveStakeholderOrganizationAccessMutation(
    $organizationId: String!
    $userEmail: String!
  ) {
    removeStakeholderOrganizationAccess(
      organizationId: $organizationId
      userEmail: $userEmail
    ) {
      success
    }
  }
`;

export {
  GET_ORGANIZATION_STAKEHOLDERS,
  ADD_STAKEHOLDER_MUTATION,
  UPDATE_STAKEHOLDER_MUTATION,
  REMOVE_STAKEHOLDER_MUTATION,
};
