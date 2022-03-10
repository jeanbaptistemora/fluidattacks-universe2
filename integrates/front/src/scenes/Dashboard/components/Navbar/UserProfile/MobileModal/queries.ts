import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_STAKEHOLDER_PHONE: DocumentNode = gql`
  query GetStakeholderPhoneQuery {
    me(callerOrigin: "FRONT") {
      phone {
        callingCountryCode
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
    $newPhone: PhoneInput!
    $verificationCode: String!
  ) {
    updateStakeholderPhone(
      phone: $newPhone
      verificationCode: $verificationCode
    ) {
      success
    }
  }
`;

const VERIFY_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation VerifyStakeholderMutation(
    $newPhone: PhoneInput
    $verificationCode: String
  ) {
    verifyStakeholder(
      newPhone: $newPhone
      verificationCode: $verificationCode
    ) {
      success
    }
  }
`;

export {
  GET_STAKEHOLDER_PHONE,
  UPDATE_STAKEHOLDER_PHONE_MUTATION,
  VERIFY_STAKEHOLDER_MUTATION,
};
