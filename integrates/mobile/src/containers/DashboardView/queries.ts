import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const ORGS_QUERY: DocumentNode = gql`{
  me {
    organizations {
      analytics(
        documentName: "remediation"
        documentType: "singleValueIndicator"
      )
      name
    }
  }
}`;

export const ADD_PUSH_TOKEN_MUTATION: DocumentNode = gql`
mutation addPushToken($token: String!) {
  addPushToken(token: $token) {
    success
  }
}`;
