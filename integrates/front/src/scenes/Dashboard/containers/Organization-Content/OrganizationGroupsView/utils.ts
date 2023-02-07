import type { ITrialData } from "./types";

import { getDatePlusDeltaDays, getRemainingDays } from "utils/date";
import { translate } from "utils/translations/translate";

const getTrialRemainingDays = (trial: ITrialData): number => {
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

const getTrialTip = (trial: ITrialData | null | undefined): string => {
  const trialDays = trial ? getTrialRemainingDays(trial) : 0;

  if (trialDays > 0) {
    return translate.t(`organization.tabs.groups.status.trialDaysTip`, {
      remainingDays: trialDays,
    });
  }

  return translate.t(`organization.tabs.groups.status.trialTip`);
};

export { getTrialTip };
