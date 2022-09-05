import { gql } from "@apollo/client";

const GET_STAKEHOLDER_WELCOME = gql`
  query GetStakeholderWelcome {
    me {
      organizations {
        groups {
          name
        }
        name
      }
      userEmail
    }
  }
`;

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

export { GET_STAKEHOLDER_WELCOME, GET_STAKEHOLDER_ENROLLMENT };
