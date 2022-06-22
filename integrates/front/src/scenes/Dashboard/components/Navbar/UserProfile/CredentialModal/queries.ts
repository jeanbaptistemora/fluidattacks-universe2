import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ADD_CREDENTIALS: DocumentNode = gql`
  mutation AddCredentialsMutation(
    $organizationId: ID!
    $credentials: CredentialsInput!
  ) {
    addCredentials(organizationId: $organizationId, credentials: $credentials) {
      success
    }
  }
`;

const GET_STAKEHOLDER_CREDENTIALS: DocumentNode = gql`
  query GetStakeholderCredentials {
    me(callerOrigin: "FRONT") {
      __typename
      credentials {
        __typename
        id
        name
        type
        organization {
          __typename
          id
          name
        }
      }
      userEmail
    }
  }
`;

const GET_STAKEHOLDER_ORGANIZATIONS: DocumentNode = gql`
  query GetStakeholderOrganizations {
    me(callerOrigin: "FRONT") {
      __typename
      organizations {
        id
        name
      }
      userEmail
    }
  }
`;

export {
  ADD_CREDENTIALS,
  GET_STAKEHOLDER_CREDENTIALS,
  GET_STAKEHOLDER_ORGANIZATIONS,
};
