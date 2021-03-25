import type { DocumentNode } from "@apollo/client";
import { gql } from "@apollo/client";

const ORGS_QUERY: DocumentNode = gql`
  {
    me {
      organizations {
        analytics(
          documentName: "remediation"
          documentType: "singleValueIndicator"
        )
        name
      }
    }
  }
`;

const ADD_PUSH_TOKEN_MUTATION: DocumentNode = gql`
  mutation addPushToken($token: String!) {
    addPushToken(token: $token) {
      success
    }
  }
`;

export { ORGS_QUERY, ADD_PUSH_TOKEN_MUTATION };
