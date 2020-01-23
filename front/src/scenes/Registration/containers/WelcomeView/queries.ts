import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_USER_AUTHORIZATION: DocumentNode = gql`
  query GetUserAuthorization {
    me {
      authorized
      remember
    }
  }
`;
