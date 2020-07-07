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
