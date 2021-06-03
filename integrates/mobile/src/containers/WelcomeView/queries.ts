import { gql } from "@apollo/client";
import type { DocumentNode } from "@apollo/client";

export const SIGN_IN_MUTATION: DocumentNode = gql`
  mutation signIn($authToken: String!, $provider: AuthProvider!) {
    signIn(authToken: $authToken, provider: $provider) {
      sessionJwt
      success
    }
  }
`;
