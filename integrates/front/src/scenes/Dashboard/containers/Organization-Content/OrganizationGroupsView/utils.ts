import _ from "lodash";

import type { IGroupData, ITrialData } from "./types";

import { getDatePlusDeltaDays, getRemainingDays } from "utils/date";
import { translate } from "utils/translations/translate";

const getTrialRemainingDays = (trial: ITrialData): number => {
  if (trial.state === "TRIAL" && trial.startDate) {
    const TRIAL_DAYS = 21;

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

const getPlan = (group: IGroupData): string => {
  const subscription = _.capitalize(group.subscription);

  if (subscription === "Oneshot") {
    return subscription;
  } else if (group.hasSquad) {
    return "Squad";
  }

  return "Machine";
};

const getEventFormat = (group: IGroupData): string => {
  if (_.isUndefined(group.events) || _.isEmpty(group.events)) {
    return "None";
  } else if (
    group.events.filter((event): boolean =>
      event.eventStatus.includes("CREATED")
    ).length > 0
  ) {
    return `${
      group.events.filter((event): boolean =>
        event.eventStatus.includes("CREATED")
      ).length
    } need(s) attention`;
  }

  return "None";
};

const formatGroupData = (groupData: IGroupData[]): IGroupData[] => {
  return groupData.map((group): IGroupData => {
    const description = _.capitalize(group.description);
    const plan = getPlan(group);
    const vulnerabilities = group.openFindings
      ? translate.t("organization.tabs.groups.vulnerabilities.open", {
          openFindings: group.openFindings,
        })
      : translate.t("organization.tabs.groups.vulnerabilities.inProcess");
    const eventFormat = getEventFormat(group);
    const status = translate.t(
      `organization.tabs.groups.status.${_.camelCase(group.managed)}`
    );

    return {
      ...group,
      description,
      eventFormat,
      plan,
      status,
      vulnerabilities,
    };
  });
};

export { formatGroupData, getTrialTip };
