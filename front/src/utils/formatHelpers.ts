import _ from "lodash";
import { IHistoricTreatment } from "../scenes/Dashboard/containers/DescriptionView/types";
import { formatHistoricTreatment } from "../scenes/Dashboard/containers/DescriptionView/utils";
import { ILastLogin, IUserDataAttr, IUsersAttr } from "../scenes/Dashboard/containers/ProjectUsersView/types";
import translate from "./translations/translate";

type IUserList = IUsersAttr["project"]["users"];

export const formatUserlist: ((userList: IUserDataAttr[]) => IUserList) =
  (userList: IUserDataAttr[]): IUserList => userList.map((user: IUserDataAttr) => {
    const lastLoginDate: number[] = JSON.parse(user.lastLogin);
    let DAYS_IN_MONTH: number;
    DAYS_IN_MONTH = 30;
    const lastLogin: ILastLogin = {
      label: "",
      value: lastLoginDate,
    };
    let firstLogin: string; firstLogin = "";
    if (!_.isUndefined(user.firstLogin)) {
      firstLogin = user.firstLogin.split(" ")[0];
    }
    if (lastLoginDate[0] >= DAYS_IN_MONTH) {
      const ROUNDED_MONTH: number = Math.round(lastLoginDate[0] / DAYS_IN_MONTH);
      lastLogin.label = translate.t("search_findings.tab_users.months_ago", { count: ROUNDED_MONTH });
    } else if (lastLoginDate[0] > 0 && lastLoginDate[0] < DAYS_IN_MONTH) {
      lastLogin.label = translate.t("search_findings.tab_users.days_ago", { count: lastLoginDate[0] });
    } else if (lastLoginDate[0] === -1) {
      lastLogin.label = "-";
      firstLogin = "-";
    } else {
      let SECONDS_IN_HOUR: number;
      SECONDS_IN_HOUR = 3600;
      const ROUNDED_HOUR: number = Math.round(lastLoginDate[1] / SECONDS_IN_HOUR);
      let SECONDS_IN_MINUTES: number;
      SECONDS_IN_MINUTES = 60;
      const ROUNDED_MINUTES: number = Math.round(lastLoginDate[1] / SECONDS_IN_MINUTES);
      lastLogin.label = ROUNDED_HOUR >= 1 && ROUNDED_MINUTES >= SECONDS_IN_MINUTES
        ? translate.t("search_findings.tab_users.hours_ago", { count: ROUNDED_HOUR })
        : translate.t("search_findings.tab_users.minutes_ago", { count: ROUNDED_MINUTES });
    }

    return { ...user, lastLogin, firstLogin };
  });

export const formatLastLogin: (value: ILastLogin) => string =
  (value: ILastLogin): string => (value.label);

export const castEventType: ((field: string) => string) = (field: string): string => {
  const eventType: {[value: string]: string} = {
    "AUTHORIZATION_SPECIAL_ATTACK": "search_findings.tab_events.type_values.auth_attack",
    "Ambiente inestable": "search_findings.tab_events.type_values.uns_ambient",
    "Ambiente no accesible": "search_findings.tab_events.type_values.inacc_ambient",
    "CLIENT_APPROVES_CHANGE_TOE": "search_findings.tab_events.type_values.approv_change",
    "CLIENT_DETECTS_ATTACK": "search_findings.tab_events.type_values.det_attack",
    "HIGH_AVAILABILITY_APPROVAL": "search_findings.tab_events.type_values.high_approval",
    "INCORRECT_MISSING_SUPPLIES": "search_findings.tab_events.type_values.incor_supplies",
    "OTHER": "search_findings.tab_events.type_values.other",
    "TOE_DIFFERS_APPROVED": "search_findings.tab_events.type_values.toe_differs",
  };

  return eventType[field];
};

export const castEventStatus: ((field: string) => string) = (field: string): string => {
  const eventStatus: {[value: string]: string} = {
    CREATED: "search_findings.tab_events.status_values.unsolve",
    SOLVED: "search_findings.tab_events.status_values.solve",
  };

  return eventStatus[field];
};

export const formatDropdownField: ((field: string) => string) = (field: string): string => {
  const translationParameters: {[value: string]: string} = {
    ACCEPTED: "search_findings.tab_description.treatment.accepted",
    ACCEPTED_UNDEFINED: "search_findings.tab_description.treatment.accepted_undefined",
    ANONYMOUS_INTERNET: "search_findings.tab_description.scenario.anon_inter",
    ANONYMOUS_INTRANET: "search_findings.tab_description.scenario.anon_intra",
    ANYONE_INTERNET: "search_findings.tab_description.actor.any_internet",
    ANYONE_WORKSTATION: "search_findings.tab_description.actor.any_station",
    ANY_CUSTOMER: "search_findings.tab_description.actor.any_customer",
    ANY_EMPLOYEE: "search_findings.tab_description.actor.any_employee",
    APPLICATIONS: "search_findings.tab_description.ambit.applications",
    AUTHORIZED_USER_EXTRANET: "search_findings.tab_description.scenario.auth_extra",
    AUTHORIZED_USER_INTERNET: "search_findings.tab_description.scenario.auth_inter",
    AUTHORIZED_USER_INTRANET: "search_findings.tab_description.scenario.auth_intra",
    DATABASES: "search_findings.tab_description.ambit.databases",
    INFRASTRUCTURE: "search_findings.tab_description.ambit.infra",
    IN_PROGRESS: "search_findings.tab_description.treatment.in_progress",
    NEW: "search_findings.tab_description.treatment.new",
    ONE_EMPLOYEE: "search_findings.tab_description.actor.one_employee",
    REJECTED: "search_findings.tab_description.treatment.rejected",
    SOME_CUSTOMERS: "search_findings.tab_description.actor.some_customer",
    SOME_EMPLOYEES: "search_findings.tab_description.actor.some_employee",
    SOURCE_CODE: "search_findings.tab_description.ambit.sourcecode",
    UNAUTHORIZED_USER_EXTRANET: "search_findings.tab_description.scenario.unauth_extra",
    UNAUTHORIZED_USER_INTERNET: "search_findings.tab_description.scenario.unauth_inter",
    UNAUTHORIZED_USER_INTRANET: "search_findings.tab_description.scenario.unauth_intra",
  };

  return translationParameters[field];
};

export const formatTreatment: ((treatment: string, findingState: string) => string) =
  (treatment: string, findingState: string): string => {
    const treatmentParameters: { [value: string]: string } = {
      "-": (findingState === "closed") ? "-" : "-",
      "ACCEPTED": (findingState === "open")
        ? "search_findings.tab_description.treatment.accepted" : "-",
      "ACCEPTED_UNDEFINED": (findingState === "open")
        ? "search_findings.tab_description.treatment.accepted_undefined" : "-",
      "ACCEPTED_UNDEFINED pending": (findingState === "open")
        ? translate.t("search_findings.tab_description.treatment.accepted_undefined") +
        translate.t("search_findings.tab_description.treatment.pending_approval") : "-",
      "IN PROGRESS": (findingState === "open")
        ? "search_findings.tab_description.treatment.in_progress" : "-",
      "NEW": (findingState === "open")
        ? "search_findings.tab_description.treatment.new" : "-",
    };
    const treatmentRes: string = translate.t(treatmentParameters[treatment]);

    return treatmentRes;
  };

export const getPreviousTreatment: ((historic: IHistoricTreatment[]) => IHistoricTreatment[]) = (
  historic: IHistoricTreatment[],
): IHistoricTreatment[] => {
  const previousTreatment: IHistoricTreatment[] = [...historic];
  previousTreatment.reverse();

  return previousTreatment.map((treatment: IHistoricTreatment) => formatHistoricTreatment(treatment, true));
};
