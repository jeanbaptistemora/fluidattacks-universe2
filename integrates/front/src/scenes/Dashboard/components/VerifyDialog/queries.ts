/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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

const VERIFY_STAKEHOLDER_MUTATION: DocumentNode = gql`
  mutation VerifyStakeholderMutation {
    verifyStakeholder {
      success
    }
  }
`;

export { GET_STAKEHOLDER_PHONE, VERIFY_STAKEHOLDER_MUTATION };
