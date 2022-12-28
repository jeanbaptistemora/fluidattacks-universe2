import _ from "lodash";

import type { ISubscriptionToEntityReport } from "scenes/Dashboard/components/ChartsGenericView/types";
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
