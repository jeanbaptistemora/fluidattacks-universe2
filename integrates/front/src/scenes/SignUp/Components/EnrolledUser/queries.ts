import { gql } from "@apollo/client";

const GET_STAKEHOLDER = gql`
  query GetStakeholder {
    me {
      userEmail
      userName
    }
  }
`;

export { GET_STAKEHOLDER };
