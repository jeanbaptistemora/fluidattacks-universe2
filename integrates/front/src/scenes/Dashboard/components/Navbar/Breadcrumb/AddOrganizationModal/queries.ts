import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_AVAILABLE_ORGANIZATION_NAME: DocumentNode = gql`
  query InternalOrganizationName {
    internalNames(entity: ORGANIZATION) {
      name
    }
  }
`;

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

export { ADD_NEW_ORGANIZATION, GET_AVAILABLE_ORGANIZATION_NAME };
