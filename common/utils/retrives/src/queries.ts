import { DocumentNode, gql } from "@apollo/client/core";

const GET_GROUPS: DocumentNode = gql`
  query GetGroups {
    me {
      userEmail
      organizations {
        groups {
          name
          subscription
        }
      }
    }
  }
`;

export { GET_GROUPS };
