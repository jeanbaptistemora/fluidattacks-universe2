import type { DocumentNode } from "graphql";
import gql from "graphql-tag";

const GET_ACCESS_TOKEN: DocumentNode = gql`
  query GetAccessTokenQuery {
    me(callerOrigin: "FRONT") {
      accessToken
    }
  }
`;

const INVALIDATE_ACCESS_TOKEN_MUTATION: DocumentNode = gql`
  mutation InvalidateAccessTokenMutation {
    invalidateAccessToken {
      success
    }
  }
`;

const UPDATE_ACCESS_TOKEN_MUTATION: DocumentNode = gql`
  mutation UpdateAccessTokenMutation($expirationTime: Int!) {
    updateAccessToken(expirationTime: $expirationTime) {
      sessionJwt
      success
    }
  }
`;

export {
  GET_ACCESS_TOKEN,
  INVALIDATE_ACCESS_TOKEN_MUTATION,
  UPDATE_ACCESS_TOKEN_MUTATION,
};
