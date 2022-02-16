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

const SUBSCRIBE_TO_ENTITY_REPORT: DocumentNode = gql`
  mutation SubscribeToEntityReport(
    $frequency: Frequency!
    $reportEntity: SubscriptionReportEntity!
    $reportSubject: String!
  ) {
    subscribeToEntityReport(
      frequency: $frequency
      reportEntity: $reportEntity
      reportSubject: $reportSubject
    ) {
      success
    }
  }
`;

export { SUBSCRIPTIONS_TO_ENTITY_REPORT, SUBSCRIBE_TO_ENTITY_REPORT };
