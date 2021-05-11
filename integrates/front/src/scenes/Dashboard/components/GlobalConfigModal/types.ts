declare type EntityType = "digest";
declare type FrequencyType = "daily" | "never";

interface IDailyDigestProps {
  entity: EntityType;
  reportMode: boolean;
  subject: string;
}

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
  IDailyDigestProps,
  ISubscriptionToEntityReport,
  ISubscriptionsToEntityReport,
};
