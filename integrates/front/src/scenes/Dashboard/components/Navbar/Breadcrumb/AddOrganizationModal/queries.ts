import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ADD_NEW_ORGANIZATION: DocumentNode = gql`
  mutation AddOrganization($country: String!, $name: String!) {
    addOrganization(country: $country, name: $name) {
      organization {
        id
        name
      }
      success
    }
  }
`;

export { ADD_NEW_ORGANIZATION };
