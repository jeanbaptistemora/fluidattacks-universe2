import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_STAKEHOLDER_PHONE: DocumentNode = gql`
  query GetStakeholderPhoneQuery {
    me(callerOrigin: "FRONT") {
      phone {
        countryCode
        localNumber
      }
      userEmail
      __typename
    }
  }
`;

const UPDATE_STAKEHOLDER_PHONE_MUTATION: DocumentNode = gql`
  mutation UpdateStakeholderPhoneMutation(
    $localNumber: String!
    $countryCode: String!
    $verificationCode: String!
  ) {
    updateStakeholderPhone(
      phone: { countryCode: $countryCode, localNumber: $localNumber }
      verificationCode: $verificationCode
    ) {
      success
    }
  }
`;

export { GET_STAKEHOLDER_PHONE, UPDATE_STAKEHOLDER_PHONE_MUTATION };
