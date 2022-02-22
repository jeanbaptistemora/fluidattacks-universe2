declare type EntityType = "digest";
declare type FrequencyType = "daily" | "never";

interface ISubscriptionNameDataSet {
  name: string;
  subscribeEmail: JSX.Element;
}

interface ISubscriptionToEntityReport {
  entity: ISubscriptionName;
  frequency: FrequencyType;
  subject: string;
}

interface ISubscriptionName {
  name: string;
}

interface ISubscriptionsNames {
  __type: {
    enumValues: ISubscriptionName[];
  };
}
interface ISubscriptionsToEntityReport {
  me: {
    subscriptionsToEntityReport: ISubscriptionToEntityReport[];
  };
}

export {
  EntityType,
  FrequencyType,
  ISubscriptionName,
  ISubscriptionNameDataSet,
  ISubscriptionsNames,
  ISubscriptionToEntityReport,
  ISubscriptionsToEntityReport,
};
