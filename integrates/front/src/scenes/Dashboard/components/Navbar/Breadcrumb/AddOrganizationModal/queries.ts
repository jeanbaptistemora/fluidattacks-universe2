import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ADD_NEW_ORGANIZATION: DocumentNode = gql`
  mutation AddOrganization($name: String!) {
    addOrganization(name: $name) {
      organization {
        id
        name
      }
      success
    }
  }
`;

export { ADD_NEW_ORGANIZATION };
