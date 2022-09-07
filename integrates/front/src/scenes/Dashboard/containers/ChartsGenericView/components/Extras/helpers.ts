/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";

import type { ISubscriptionToEntityReport } from "scenes/Dashboard/containers/ChartsGenericView/types";
import { translate } from "utils/translations/translate";

const translateFrequency = (
  freq: string,
  kind: "action" | "statement"
): string =>
  translate.t(`analytics.sections.extras.frequencies.${kind}.${freq}`);

const translateFrequencyArrivalTime: (freq: string) => string = (
  freq: string
): string =>
  translate.t(`analytics.sections.extras.frequenciesArrivalTime.${freq}`);

const getSubscriptionFrequency = (
  subscriptions: ISubscriptionToEntityReport[]
): string =>
  _.isEmpty(subscriptions) ? "never" : subscriptions[0].frequency.toLowerCase();

export {
  translateFrequency,
  translateFrequencyArrivalTime,
  getSubscriptionFrequency,
};
