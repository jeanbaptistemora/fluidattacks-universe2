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

export { GET_USER_WELCOME };
