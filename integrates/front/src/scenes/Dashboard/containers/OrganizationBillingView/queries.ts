import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_ORGANIZATION_BILLING: DocumentNode = gql`
  query GetOrganizationBilling($organizationId: String!) {
    organization(organizationId: $organizationId) {
      name
      groups {
        name
        hasForces
        hasMachine
        hasSquad
        service
        tier
      }
      billingPaymentMethods {
        id
        brand
        default
        expirationMonth
        expirationYear
        lastFourDigits
      }
    }
  }
`;

const ADD_BILLING_PAYMENT_METHOD: DocumentNode = gql`
  mutation addBillingPaymentMethod(
    $organizationId: String!
    $cardNumber: String!
    $cardExpirationMonth: String!
    $cardExpirationYear: String!
    $cardCvc: String!
    $makeDefault: Boolean!
  ) {
    addBillingPaymentMethod(
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

const REMOVE_BILLING_PAYMENT_METHOD: DocumentNode = gql`
  mutation removeBillingPaymentMethod(
    $organizationId: String!
    $paymentMethodId: String!
  ) {
    removeBillingPaymentMethod(
      organizationId: $organizationId
      paymentMethodId: $paymentMethodId
    ) {
      success
    }
  }
`;

export {
  ADD_BILLING_PAYMENT_METHOD,
  GET_ORGANIZATION_BILLING,
  REMOVE_BILLING_PAYMENT_METHOD,
};
