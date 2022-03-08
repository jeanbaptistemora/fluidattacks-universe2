import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_STAKEHOLDER_PHONE_NUMBER: DocumentNode = gql`
  query GetStakeholderPhoneNumberQuery {
    me(callerOrigin: "FRONT") {
      phoneNumber
      userEmail
      __typename
    }
  }
`;

const UPDATE_STAKEHOLDER_PHONE_NUMBER_MUTATION: DocumentNode = gql`
  mutation UpdateStakeholderPhoneNumberMutation(
    $phoneNumber: string!
    $verificationCode: string!
  ) {
    updateStakeholderPhoneNumber(
      phoneNumber: $phoneNumber
      verificationCode: $verificationCode
    ) {
      success
    }
  }
`;

export {
  GET_STAKEHOLDER_PHONE_NUMBER,
  UPDATE_STAKEHOLDER_PHONE_NUMBER_MUTATION,
};
