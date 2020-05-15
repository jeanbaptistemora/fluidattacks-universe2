import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const SIGN_IN_MUTATION: DocumentNode = gql`
mutation signIn($authToken: String!, $provider: String!) {
  signIn(authToken: $authToken, provider: $provider) {
    authorized
    sessionJwt
    success
  }
}`;
