import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_SUBSCRIPTIONS: DocumentNode = gql`
  query GetSubscriptions {
    Notifications: __type(name: "NotificationsName") {
      enumValues {
        name
      }
    }
    me {
      notificationsPreferences {
        email
      }
      userEmail
    }
  }
`;

const UPDATE_NOTIFICATIONS_PREFERENCES: DocumentNode = gql`
  mutation UpdateNotificationsPreferences(
    $notificationsPreferences: [NotificationsName!]!
  ) {
    updateNotificationsPreferences(
      notificationsPreferences: { email: $notificationsPreferences }
    ) {
      success
    }
  }
`;

export { GET_SUBSCRIPTIONS, UPDATE_NOTIFICATIONS_PREFERENCES };
