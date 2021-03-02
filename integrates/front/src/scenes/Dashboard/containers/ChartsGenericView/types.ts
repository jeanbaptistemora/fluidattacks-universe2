declare type EntityType = "group" | "organization" | "portfolio";
declare type FrequencyType =
  | "daily"
  | "hourly"
  | "monthly"
  | "never"
  | "weekly";

interface IChartsGenericViewProps {
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
  IChartsGenericViewProps,
  ISubscriptionToEntityReport,
  ISubscriptionsToEntityReport,
};
