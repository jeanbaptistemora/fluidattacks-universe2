export declare type EntityType = "group" | "organization" | "portfolio";
export declare type FrequencyType = "hourly" | "daily" | "weekly" | "monthly" | "never";

export interface IChartsGenericViewProps {
  entity: EntityType;
  reportMode: boolean;
  subject: string;
}

export interface ISubscriptionToEntityReport {
  entity: EntityType;
  frequency: FrequencyType;
  subject: string;
}

export interface ISubscriptionsToEntityReport {
  me: {
    subscriptionsToEntityReport: ISubscriptionToEntityReport[];
  };
}
