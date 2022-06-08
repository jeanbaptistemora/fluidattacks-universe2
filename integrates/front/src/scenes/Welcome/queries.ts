import { gql } from "@apollo/client";

const GET_USER_WELCOME = gql`
  query GetUserWelcome {
    me {
      organizations {
        name
      }
      userEmail
      userName
    }
  }
`;

export { GET_USER_WELCOME };
