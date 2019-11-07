import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_ACCESS_TOKEN: DocumentNode = gql`
  query GetAccessTokenQuery {
    me {
      accessToken
    }
  }`;

export const INVALIDATE_ACCESS_TOKEN_MUTATION: DocumentNode = gql`
  mutation UpdateAccessTokenMutation {
    invalidateAccessToken {
      success
    }
  }
  `;

export const UPDATE_ACCESS_TOKEN_MUTATION: DocumentNode = gql`
  mutation UpdateAccessTokenMutation($expirationTime: Int!) {
    updateAccessToken (expirationTime: $expirationTime) {
      sessionJwt
      success
    }
  }
  `;
