/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface INotificationsPreferences {
  email: string[];
  sms: string[];
  parameters: {
    minSeverity: number;
  };
}

interface ISubscriptionName {
  minSeverity: JSX.Element;
  name: string;
  subscribeEmail: JSX.Element;
  subscribeSms: JSX.Element;
  tooltip: string;
}

interface ISubscriptionsNames {
  Notifications: {
    enumValues: ISubscriptionName[];
  };
  me: {
    notificationsPreferences: INotificationsPreferences;
    userEmail: string;
  };
}

export type { ISubscriptionName, ISubscriptionsNames };
