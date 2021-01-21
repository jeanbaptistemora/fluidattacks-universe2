import type { DocumentNode } from "graphql";
import gql from "graphql-tag";

const GET_USER_AUTHORIZATION: DocumentNode = gql`
  query GetUserAuthorization {
    me(callerOrigin: "FRONT") {
      remember
    }
  }
`;

const ACCEPT_LEGAL_MUTATION: DocumentNode = gql`
  mutation AcceptLegalMutation($remember: Boolean!) {
    acceptLegal(remember: $remember) {
      success
    }
  }
`;

export { GET_USER_AUTHORIZATION, ACCEPT_LEGAL_MUTATION };
