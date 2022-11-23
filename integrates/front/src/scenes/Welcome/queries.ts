import { gql } from "@apollo/client";

const GET_STAKEHOLDER_ENROLLMENT = gql`
  query GetStakeholderEnrollment {
    me {
      enrollment {
        enrolled
      }
      userEmail
      userName
    }
  }
`;

export { GET_STAKEHOLDER_ENROLLMENT };
