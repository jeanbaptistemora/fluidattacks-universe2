import { gql } from "@apollo/client";

const GET_STAKEHOLDER_WELCOME = gql`
  query GetStakeholderWelcome {
    me {
      organizations {
        groups {
          name
          roots {
            ... on GitRoot {
              url
            }
          }
          service
          subscription
        }
        name
      }
      remember
      userEmail
      userName
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
    }
  }
`;

export { GET_STAKEHOLDER_WELCOME, GET_STAKEHOLDER_ENROLLMENT };
