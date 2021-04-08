import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_USER_ORGANIZATIONS: DocumentNode = gql`
  query GetUserOrganizations {
    me(callerOrigin: "FRONT") {
      organizations {
        name
      }
    }
  }
`;
