import { gql } from "@apollo/client";

const GET_USER_WELCOME = gql`
  query GetUserWelcome {
    me {
      organizations {
        groups {
          name
          roots {
            ... on GitRoot {
              url
            }
          }
        }
        name
      }
      userEmail
      userName
    }
  }
`;

export { GET_USER_WELCOME };
