import { gql } from "@apollo/client";

const GET_STAKEHOLDER_ENROLLMENT = gql`
  query GetStakeholderEnrollment {
    me {
      enrolled
      organizations {
        groups {
          managed
          name
        }
        name
      }
      trial {
        completed
      }
      userEmail
      userName
    }
  }
`;

export { GET_STAKEHOLDER_ENROLLMENT };
