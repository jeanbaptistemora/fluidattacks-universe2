import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_STAKEHOLDER_CREDENTIALS: DocumentNode = gql`
  query GetStakeholderCredentials {
    me(callerOrigin: "FRONT") {
      __typename
      credentials {
        __typename
        id
        name
        type
        organization {
          __typename
          id
          name
        }
      }
      userEmail
    }
  }
`;

export { GET_STAKEHOLDER_CREDENTIALS };
