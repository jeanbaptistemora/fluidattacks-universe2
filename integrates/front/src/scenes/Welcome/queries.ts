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

export { ADD_ORGANIZATION, AUTOENROLL_DEMO, GET_USER_WELCOME };
