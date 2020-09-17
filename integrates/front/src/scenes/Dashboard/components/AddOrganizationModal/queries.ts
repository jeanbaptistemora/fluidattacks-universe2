import { DocumentNode } from "graphql";
import gql from "graphql-tag";

const GET_AVAILABLE_ORGANIZATION_NAME: DocumentNode = gql`
  query InternalOrganizationName {
    internalNames(entity: ORGANIZATION) {
      name
    }
  }
`;

const CREATE_NEW_ORGANIZATION: DocumentNode = gql`
  mutation CreateOrganization($name: String!) {
    createOrganization(name: $name) {
      organization {
        id
        name
      }
      success
    }
  }
`;

export { CREATE_NEW_ORGANIZATION, GET_AVAILABLE_ORGANIZATION_NAME };
