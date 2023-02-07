import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const SUBSCRIPTIONS_TO_ENTITY_REPORT: DocumentNode = gql`
  query SubscriptionsToEntityReport {
    me {
      subscriptionsToEntityReport {
        entity
        frequency
        subject
      }
      userEmail
    }
  }
`;

const GET_VULNERABILITIES_URL: DocumentNode = gql`
  query GetOrgVulnerabilitiesUrl(
    $identifier: String!
    $verificationCode: String
  ) {
    organization(organizationId: $identifier) {
      name
      vulnerabilitiesUrl(verificationCode: $verificationCode)
    }
  }
`;

export { GET_VULNERABILITIES_URL, SUBSCRIPTIONS_TO_ENTITY_REPORT };
