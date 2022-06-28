interface INotificationsPreferences {
  email: string[];
  sms: string[];
}

interface ISubscriptionName {
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
