import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const SEND_SALES_EMAIL_TO_GET_SQUAD_PLAN: DocumentNode = gql`
  mutation SendSalesMailToGetSquadPlan(
    $phone: PhoneInput!
    $name: String!
    $email: String!
  ) {
    sendSalesMailToGetSquadPlan(email: $email, name: $name, phone: $phone) {
      success
    }
  }
`;

const GET_STAKEHOLDER = gql`
  query GetStakeholderEnrollment {
    me {
      userEmail
      userName
    }
  }
`;

export { SEND_SALES_EMAIL_TO_GET_SQUAD_PLAN, GET_STAKEHOLDER };
