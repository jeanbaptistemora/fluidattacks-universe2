import { gql } from "@apollo/client";

const GET_USER_WELCOME = gql`
  query GetUserWelcome {
    me {
      organizations {
        name
      }
      userEmail
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

const AUTOENROLL_DEMO = gql`
  mutation AutoenrollDemo {
    autoenrollDemo {
      success
    }
  }
`;

export {
  ADD_ORGANIZATION,
  AUTOENROLL_DEMO,
  GET_NEW_ORGANIZATION_NAME,
  GET_USER_WELCOME,
};
