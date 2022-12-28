/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { TFunction } from "react-i18next";

import type { ITrialData } from "./types";

import { getDatePlusDeltaDays, getRemainingDays } from "utils/date";

const getTrialRemainingDays = (trialData: ITrialData): number => {
  const { trial } = trialData;
  if (trial.state === "TRIAL" && trial.startDate) {
    const TRIAL_DAYS: number = 21;

    return getRemainingDays(getDatePlusDeltaDays(trial.startDate, TRIAL_DAYS));
  }
  if (trial.state === "EXTENDED" && trial.extensionDate) {
    return getRemainingDays(
      getDatePlusDeltaDays(trial.extensionDate, trial.extensionDays)
    );
  }

  return 0;
};

const getTrialTip = (
  trialData: ITrialData | undefined,
  t: TFunction
): string => {
  const trialDays =
    trialData === undefined ? 0 : getTrialRemainingDays(trialData);
  if (trialDays > 0) {
    return t(`organization.tabs.groups.status.trialDaysTip`, {
      remainingDays: trialDays,
    });
  }

  return t(`organization.tabs.groups.status.trialTip`);
};

export { getTrialTip };
