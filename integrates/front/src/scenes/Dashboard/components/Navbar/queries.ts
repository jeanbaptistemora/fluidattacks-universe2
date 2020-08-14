import { DocumentNode } from "graphql";
import gql from "graphql-tag";

export const GET_USER_ORGANIZATIONS: DocumentNode = gql`
  query GetUserOrganizations {
    me(callerOrigin: "FRONT") {
      organizations {
        name
      }
    }
  }
`;
