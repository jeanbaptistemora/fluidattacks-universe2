import { gql } from "@apollo/client";

const GET_USER_WELCOME = gql`
  query GetUserWelcome {
    me {
      userEmail
      organizations {
        name
      }
    }
  }
`;

const GET_NEW_ORGANIZATION_NAME = gql`
  query GetNewOrganizationName {
    internalNames(entity: ORGANIZATION) {
      name
    }
  }
`;

const ADD_ORGANIZATION = gql`
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

export { ADD_ORGANIZATION, GET_NEW_ORGANIZATION_NAME, GET_USER_WELCOME };
