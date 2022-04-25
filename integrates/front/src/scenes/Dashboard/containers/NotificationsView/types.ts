interface ISubscriptionName {
  name: string;
  subscribeEmail: JSX.Element;
  tooltip: string;
}

interface ISubscriptionsNames {
  Notifications: {
    enumValues: ISubscriptionName[];
  };
  me: {
    notificationsPreferences: {
      email: string[];
    };
    userEmail: string;
  };
}

export type { ISubscriptionName, ISubscriptionsNames };
