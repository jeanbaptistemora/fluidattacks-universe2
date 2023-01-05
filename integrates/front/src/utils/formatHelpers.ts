import { isValidElement } from "react";

const castEventType: (field: string) => string = (field: string): string => {
  const eventType: Record<string, string> = {
    AUTHORIZATION_SPECIAL_ATTACK:
      "group.events.type.authorizationSpecialAttack",
    CLIENT_CANCELS_PROJECT_MILESTONE:
      "group.events.type.clientCancelsProjectMilestone",
    CLIENT_EXPLICITLY_SUSPENDS_PROJECT:
      "group.events.type.clientSuspendsProject",
    CLONING_ISSUES: "group.events.type.cloningIssues",
    CREDENTIAL_ISSUES: "group.events.type.credentialsIssues",
    DATA_UPDATE_REQUIRED: "group.events.type.dataUpdateRequired",
    ENVIRONMENT_ISSUES: "group.events.type.environmentIssues",
    INSTALLER_ISSUES: "group.events.type.installerIssues",
    MISSING_SUPPLIES: "group.events.type.missingSupplies",
    NETWORK_ACCESS_ISSUES: "group.events.type.networkAccessIssues",
    OTHER: "group.events.type.other",
    REMOTE_ACCESS_ISSUES: "group.events.type.remoteAccessIssues",
    TOE_DIFFERS_APPROVED: "group.events.type.toeDiffersApproved",
    VPN_ISSUES: "group.events.type.vpnIssues",
  };

  return eventType[field];
};

const castEventStatus: (field: string) => string = (field: string): string => {
  const eventStatus: Record<string, string> = {
    CREATED: "searchFindings.tabEvents.statusValues.unsolve",
    SOLVED: "searchFindings.tabEvents.statusValues.solve",
    VERIFICATION_REQUESTED:
      "searchFindings.tabEvents.statusValues.pendingVerification",
  };

  return eventStatus[field];
};

const formatDropdownField: (field: string) => string = (
  field: string
): string => {
  const translationParameters: Record<string, string> = {
    ACCEPTED: "searchFindings.tabDescription.treatment.accepted",
    ACCEPTED_UNDEFINED:
      "searchFindings.tabDescription.treatment.acceptedUndefined",
    APPLICATIONS: "searchFindings.tabDescription.ambit.applications",
    DATABASES: "searchFindings.tabDescription.ambit.databases",
    INFRASTRUCTURE: "searchFindings.tabDescription.ambit.infra",
    IN_PROGRESS: "searchFindings.tabDescription.treatment.inProgress",
    NEW: "searchFindings.tabDescription.treatment.new",
    REJECTED: "searchFindings.tabDescription.treatment.rejected",
    SOURCE_CODE: "searchFindings.tabDescription.ambit.sourcecode",
  };

  return translationParameters[field];
};

const formatDate: (date: number | string) => string = (
  date: number | string
): string => {
  if (date < 0) {
    return "-";
  }
  const dateObj: Date = new Date(date);

  const toStringAndPad: (input: number, positions: number) => string = (
    input: number,
    positions: number
  ): string => input.toString().padStart(positions, "0");

  const year: string = toStringAndPad(dateObj.getFullYear(), 4);
  // Warning: months are 0 indexed: January is 0, December is 11
  const month: string = toStringAndPad(dateObj.getMonth() + 1, 2);
  // Warning: Date.getDay() returns the day of the week: Monday is 1, Friday is 5
  const day: string = toStringAndPad(dateObj.getDate(), 2);
  const hours: string = toStringAndPad(dateObj.getHours(), 2);
  const minutes: string = toStringAndPad(dateObj.getMinutes(), 2);

  return `${year}-${month}-${day} ${hours}:${minutes}`;
};

const formatDuration = (value: number): string => {
  if (value < 0) {
    return "-";
  }
  const secondsInMili = 1000;
  const factor = 60;

  const seconds = Math.trunc(value / secondsInMili);
  const minutes = Math.trunc(seconds / factor);
  const ss = seconds % factor;
  const hh = Math.trunc(minutes / factor);
  const mm = minutes % factor;
  const hhStr = hh.toString().length < 2 ? `0${hh}` : hh.toString();
  const mmStr = mm.toString().length < 2 ? `0${mm}` : mm.toString();
  const ssStr = ss.toString().length < 2 ? `0${ss}` : ss.toString();

  return `${hhStr}:${mmStr}:${ssStr}`;
};

const flattenObj = (input: object): object => {
  const traverseKeys = (
    prevKey: string,
    entries: [string, unknown][]
  ): [string, unknown][] => {
    const ent = entries.reduce(
      (
        current: [string, unknown][],
        [key, value]: [string, unknown]
      ): [string, unknown][] => {
        if (isValidElement(value) || key === "__typename")
          return current.concat([["", ""]]);
        if (typeof value === "object" && value) {
          const objEntries: [string, unknown][] = Object.entries(value);

          return current.concat(traverseKeys(key, objEntries));
        }
        const path = prevKey === "" ? "" : `${prevKey}.`;

        return current.concat([[path + key, value]]);
      },
      []
    );

    return ent;
  };
  const entries: [string, unknown][] = Object.entries(input);
  const flatEntries = traverseKeys("", entries).filter(
    ([key, _value]: [string, unknown]): boolean => key !== ""
  );

  return Object.fromEntries(flatEntries);
};

const flattenData = (dataset: object[]): object[] => {
  const flatArray: object[] = dataset.map((datapoint: object): object => {
    return flattenObj(datapoint);
  });

  return flatArray;
};

export {
  castEventType,
  castEventStatus,
  flattenData,
  flattenObj,
  formatDate,
  formatDropdownField,
  formatDuration,
};
