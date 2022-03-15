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
    userEmail: string;
  };
}

export { ISubscriptionName, ISubscriptionsNames };
