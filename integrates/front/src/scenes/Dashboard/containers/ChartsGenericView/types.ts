/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

declare type EntityType = "group" | "organization" | "portfolio";
declare type FrequencyType =
  | "daily"
  | "hourly"
  | "monthly"
  | "never"
  | "weekly";

interface IChartsGenericViewProps {
  bgChange: boolean;
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

export type {
  EntityType,
  FrequencyType,
  IChartsGenericViewProps,
  ISubscriptionToEntityReport,
  ISubscriptionsToEntityReport,
};
