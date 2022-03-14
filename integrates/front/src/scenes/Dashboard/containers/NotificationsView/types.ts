interface ISubscriptionName {
  name: string;
  subscribeEmail: JSX.Element;
}

interface ISubscriptionsNames {
  Notifications: {
    enumValues: ISubscriptionName[];
  };
  me: {
    notificationsPreferences: {
      email: string[];
    };
  };
}

export { ISubscriptionName, ISubscriptionsNames };
