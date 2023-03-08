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

export type {
  INotificationsPreferences,
  ISubscriptionName,
  ISubscriptionsNames,
};
