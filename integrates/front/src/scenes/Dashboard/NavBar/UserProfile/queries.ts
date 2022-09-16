/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */
import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_STAKEHOLDER: DocumentNode = gql`
  query GetStakeholderDataQuery(
    $entity: StakeholderEntity!
    $organizationId: String
    $groupName: String
    $userEmail: String!
  ) {
    stakeholder(
      entity: $entity
      organizationId: $organizationId
      groupName: $groupName
      userEmail: $userEmail
    ) {
      email
      responsibility
    }
  }
`;

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

const REMOVE_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation RemoveStakeholderMutation {
    removeStakeholder {
      success
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
  GET_STAKEHOLDER,
  GET_STAKEHOLDER_PHONE,
  REMOVE_STAKEHOLDER_MUTATION,
  UPDATE_STAKEHOLDER_PHONE_MUTATION,
  VERIFY_STAKEHOLDER_MUTATION,
};
