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

const GET_ORGANIZATION_CREDENTIALS: DocumentNode = gql`
  query GetOrganizationCredentials($organizationId: String!) {
    organization(organizationId: $organizationId) {
      __typename
      name
      credentials {
        __typename
        azureOrganization
        id
        isPat
        isToken
        name
        owner
        type
      }
    }
  }
`;

const REMOVE_CREDENTIALS: DocumentNode = gql`
  mutation RemoveCredentialsMutation(
    $organizationId: ID!
    $credentialsId: ID!
  ) {
    removeCredentials(
      organizationId: $organizationId
      credentialsId: $credentialsId
    ) {
      success
    }
  }
`;

const UPDATE_CREDENTIALS: DocumentNode = gql`
  mutation UpdateCredentialsMutation(
    $credentialsId: ID!
    $organizationId: ID!
    $credentials: CredentialsInput!
  ) {
    updateCredentials(
      credentialsId: $credentialsId
      organizationId: $organizationId
      credentials: $credentials
    ) {
      success
    }
  }
`;

export {
  ADD_CREDENTIALS,
  GET_ORGANIZATION_CREDENTIALS,
  REMOVE_CREDENTIALS,
  UPDATE_CREDENTIALS,
};
