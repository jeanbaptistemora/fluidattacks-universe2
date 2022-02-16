declare type EntityType = "digest";
declare type FrequencyType = "daily" | "never";

interface ISubscriptionToEntityReport {
  entity: EntityType;
  frequency: FrequencyType;
  subject: string;
}

interface ISubscriptionsToEntityReport {
  me: {
    subscriptionsToEntityReport: ISubscriptionToEntityReport[];
  };
}

export {
  EntityType,
  FrequencyType,
  ISubscriptionToEntityReport,
  ISubscriptionsToEntityReport,
};
