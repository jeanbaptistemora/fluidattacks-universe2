import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_USER_AUTHORIZATION: DocumentNode = gql`
  query GetUserAuthorization {
    me(callerOrigin: "FRONT") {
      authorized
      remember
    }
  }
`;

export const ACCEPT_LEGAL_MUTATION: DocumentNode = gql`
  mutation AcceptLegalMutation($remember: Boolean!) {
    acceptLegal(remember: $remember) {
      success
    }
  }
`;
