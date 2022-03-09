import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_STAKEHOLDER_PHONE: DocumentNode = gql`
  query GetStakeholderPhoneQuery {
    me(callerOrigin: "FRONT") {
      phone {
        countryCode
        nationalNumber
      }
      userEmail
      __typename
    }
  }
`;

const UPDATE_STAKEHOLDER_PHONE_MUTATION: DocumentNode = gql`
  mutation UpdateStakeholderPhoneMutation(
    $nationalNumber: String!
    $countryCode: String!
    $verificationCode: String!
  ) {
    updateStakeholderPhone(
      phone: { countryCode: $countryCode, nationalNumber: $nationalNumber }
      verificationCode: $verificationCode
    ) {
      success
    }
  }
`;

export { GET_STAKEHOLDER_PHONE, UPDATE_STAKEHOLDER_PHONE_MUTATION };
