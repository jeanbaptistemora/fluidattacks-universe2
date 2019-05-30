import { DocumentNode, gql } from "apollo-boost";

export const SIGN_IN_MUTATION: DocumentNode = gql`mutation signIn($authToken: String!, $provider: String!) {
  signIn(authToken: $authToken, provider: $provider) {
    authorized
    sessionJwt
    success
  }
}`;
