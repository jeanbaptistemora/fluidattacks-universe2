import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const SIGN_IN_MUTATION: DocumentNode = gql`
mutation signIn($authToken: String!, $provider: AuthProvider!) {
  signIn(authToken: $authToken, provider: $provider) {
    sessionJwt
    success
  }
}`;
