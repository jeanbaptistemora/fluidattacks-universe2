import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const DOWNLOAD_FILE_MUTATION: DocumentNode = gql`
  mutation DownloadBillingFileMutation(
    $organizationId: String!
    $paymentMethodId: String!
    $fileName: String!
  ) {
    downloadBillingFile(
      organizationId: $organizationId
      paymentMethodId: $paymentMethodId
      fileName: $fileName
    ) {
      success
      url
    }
  }
`;

const GET_ORGANIZATION_BILLING: DocumentNode = gql`
  query GetOrganizationBilling($organizationId: String!) {
    organization(organizationId: $organizationId) {
      name
      billing {
        authors {
          actor
          activeGroups {
            name
            tier
          }
        }
        costsAuthors
        costsBase
        costsTotal
        numberAuthorsMachine
        numberAuthorsSquad
        numberAuthorsTotal
        numberGroupsMachine
        numberGroupsSquad
        numberGroupsTotal
        paymentMethods {
          businessName
          id
          brand
          default
          expirationMonth
          expirationYear
          lastFourDigits
          email
          country
          state
          city
          rut {
            fileName
            modifiedDate
          }
          taxId {
            fileName
            modifiedDate
          }
        }
        portal
      }
      groups {
        name
        hasForces
        hasMachine
        hasSquad
        managed
        service
        paymentId
        permissions
        tier
        billing {
          costsAuthors
          costsBase
          costsTotal
          numberAuthors
        }
      }
    }
  }
`;

const ADD_PAYMENT_METHOD: DocumentNode = gql`
  mutation addPaymentMethod(
    $organizationId: String!
    $cardNumber: String!
    $cardExpirationMonth: String!
    $cardExpirationYear: String!
    $cardCvc: String!
    $makeDefault: Boolean!
    $businessName: String!
    $email: String!
    $country: String!
    $state: String!
    $city: String!
    $rut: Upload
    $taxId: Upload
  ) {
    addPaymentMethod(
      organizationId: $organizationId
      cardNumber: $cardNumber
      cardExpirationMonth: $cardExpirationMonth
      cardExpirationYear: $cardExpirationYear
      cardCvc: $cardCvc
      makeDefault: $makeDefault
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

const REMOVE_PAYMENT_METHOD: DocumentNode = gql`
  mutation removePaymentMethod(
    $organizationId: String!
    $paymentMethodId: String!
  ) {
    removePaymentMethod(
      organizationId: $organizationId
      paymentMethodId: $paymentMethodId
    ) {
      success
    }
  }
`;

const UPDATE_PAYMENT_METHOD: DocumentNode = gql`
  mutation updatePaymentMethod(
    $organizationId: String!
    $paymentMethodId: String!
    $cardExpirationMonth: String!
    $cardExpirationYear: String!
    $makeDefault: Boolean!
    $businessName: String!
    $email: String!
    $country: String!
    $state: String!
    $city: String!
    $rut: Upload
    $taxId: Upload
  ) {
    updatePaymentMethod(
      organizationId: $organizationId
      paymentMethodId: $paymentMethodId
      cardExpirationMonth: $cardExpirationMonth
      cardExpirationYear: $cardExpirationYear
      makeDefault: $makeDefault
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

const UPDATE_SUBSCRIPTION: DocumentNode = gql`
  mutation updateSubscription(
    $groupName: String!
    $subscription: BillingSubscriptionType!
  ) {
    updateSubscription(groupName: $groupName, subscription: $subscription) {
      success
    }
  }
`;

const UPDATE_GROUP_MUTATION: DocumentNode = gql`
  mutation UpdateGroupMutation(
    $comments: String!
    $groupName: String!
    $isPaymentIdChanged: Boolean!
    $isSubscriptionChanged: Boolean!
    $paymentId: String!
    $subscription: BillingSubscriptionType!
  ) {
    updateGroupPaymentId(
      comments: $comments
      groupName: $groupName
      paymentId: $paymentId
    ) @include(if: $isPaymentIdChanged) {
      success
    }
    updateSubscription(groupName: $groupName, subscription: $subscription)
      @include(if: $isSubscriptionChanged) {
      success
    }
  }
`;

export {
  ADD_PAYMENT_METHOD,
  DOWNLOAD_FILE_MUTATION,
  GET_ORGANIZATION_BILLING,
  REMOVE_PAYMENT_METHOD,
  UPDATE_GROUP_MUTATION,
  UPDATE_PAYMENT_METHOD,
  UPDATE_SUBSCRIPTION,
};
