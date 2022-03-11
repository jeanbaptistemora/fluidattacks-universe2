interface ISubscriptionNameDataSet {
  name: string;
  subscribeEmail: JSX.Element;
}

interface ISubscriptionName {
  name: string;
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

export { ISubscriptionName, ISubscriptionNameDataSet, ISubscriptionsNames };
