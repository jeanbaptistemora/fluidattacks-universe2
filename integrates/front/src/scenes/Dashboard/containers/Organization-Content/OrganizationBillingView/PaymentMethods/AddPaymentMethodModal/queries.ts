import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const ADD_CREDIT_CARD_PAYMENT_METHOD: DocumentNode = gql`
  mutation addCreditCardPaymentMethod(
    $organizationId: String!
    $cardNumber: String!
    $cardExpirationMonth: String!
    $cardExpirationYear: String!
    $cardCvc: String!
    $makeDefault: Boolean!
  ) {
    addCreditCardPaymentMethod(
      organizationId: $organizationId
      cardNumber: $cardNumber
      cardExpirationMonth: $cardExpirationMonth
      cardExpirationYear: $cardExpirationYear
      cardCvc: $cardCvc
      makeDefault: $makeDefault
    ) {
      success
    }
  }
`;

const ADD_OTHER_PAYMENT_METHOD: DocumentNode = gql`
  mutation addOtherPaymentMethod(
    $organizationId: String!
    $businessName: String!
    $email: String!
    $country: String!
    $state: String!
    $city: String!
    $rut: Upload
    $taxId: Upload
  ) {
    addOtherPaymentMethod(
      organizationId: $organizationId
      businessName: $businessName
      email: $email
      country: $country
      state: $state
      city: $city
      rut: $rut
      taxId: $taxId
    ) {
      success
    }
  }
`;

export { ADD_CREDIT_CARD_PAYMENT_METHOD, ADD_OTHER_PAYMENT_METHOD };
