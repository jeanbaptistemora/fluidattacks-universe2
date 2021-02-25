import type { DocumentNode } from "graphql";
import gql from "graphql-tag";

const SUBSCRIPTIONS_TO_ENTITY_REPORT: DocumentNode = gql`
  query SubscriptionsToEntityReport {
    me {
      subscriptionsToEntityReport {
        entity
        frequency
        subject
      }
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
