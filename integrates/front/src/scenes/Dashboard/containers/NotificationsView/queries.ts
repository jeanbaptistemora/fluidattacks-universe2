/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
        sms
        parameters {
          minSeverity
        }
      }
      userEmail
    }
  }
`;

const UPDATE_NOTIFICATIONS_PREFERENCES: DocumentNode = gql`
  mutation UpdateNotificationsPreferences(
    $email: [NotificationsName!]!
    $severity: Float!
    $sms: [NotificationsName]
  ) {
    updateNotificationsPreferences(
      notificationsPreferences: {
        email: $email
        parameters: { minSeverity: $severity }
        sms: $sms
      }
    ) {
      success
    }
  }
`;

export { GET_SUBSCRIPTIONS, UPDATE_NOTIFICATIONS_PREFERENCES };
