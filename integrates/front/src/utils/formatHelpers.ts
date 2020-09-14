import _ from "lodash";
import { translate } from "utils/translations/translate";
import {
  ILastLogin,
  IStakeholderAttr,
  IStakeholderDataAttr,
} from "scenes/Dashboard/containers/ProjectStakeholdersView/types";

type User = IStakeholderAttr["project"]["stakeholders"][0];

const formatUserlist: (userList: IStakeholderDataAttr[]) => User[] = (
  userList: IStakeholderDataAttr[]
): User[] =>
  userList.map(
    (user: IStakeholderDataAttr): User => {
      const missing: number = -1;
      const lastLoginDate: number[] = JSON.parse(user.lastLogin);
      const daysInMonth: number = 30;

      const firstLogin: string = ((): string => {
        if (lastLoginDate[0] === missing) {
          return "-";
        }
        if (!_.isUndefined(user.firstLogin)) {
          return user.firstLogin.split(" ")[0];
        }

        return "";
      })();

      const lastLogin: ILastLogin = {
        label: ((): string => {
          if (lastLoginDate[0] >= daysInMonth) {
            return translate.t("search_findings.tab_users.months_ago", {
              count: Math.round(lastLoginDate[0] / daysInMonth),
            });
          }
          if (lastLoginDate[0] > 0) {
            return translate.t("search_findings.tab_users.days_ago", {
              count: lastLoginDate[0],
            });
          }
          if (lastLoginDate[0] === missing) {
            return "-";
          }
          const secsInMin: number = 60;
          const secsInHour: number = 3600;
          const roundedMinutes: number = Math.round(
            lastLoginDate[1] / secsInMin
          );
          const roundedHour: number = Math.round(lastLoginDate[1] / secsInHour);

          return roundedHour >= 1 && roundedMinutes >= secsInMin
            ? translate.t("search_findings.tab_users.hours_ago", {
                count: roundedHour,
              })
            : translate.t("search_findings.tab_users.minutes_ago", {
                count: roundedMinutes,
              });
        })(),
        value: lastLoginDate,
      };

      return { ...user, firstLogin, lastLogin };
    }
  );

const formatLastLogin: (value: ILastLogin) => string = (
  value: ILastLogin
): string => value.label;

const castEventType: (field: string) => string = (field: string): string => {
  const eventType: Record<string, string> = {
    AUTHORIZATION_SPECIAL_ATTACK:
      "search_findings.tab_events.type_values.auth_attack",
    "Ambiente inestable": "search_findings.tab_events.type_values.uns_ambient",
    "Ambiente no accesible":
      "search_findings.tab_events.type_values.inacc_ambient",
    CLIENT_APPROVES_CHANGE_TOE:
      "search_findings.tab_events.type_values.approv_change",
    CLIENT_DETECTS_ATTACK: "search_findings.tab_events.type_values.det_attack",
    HIGH_AVAILABILITY_APPROVAL:
      "search_findings.tab_events.type_values.high_approval",
    INCORRECT_MISSING_SUPPLIES:
      "search_findings.tab_events.type_values.incor_supplies",
    OTHER: "search_findings.tab_events.type_values.other",
    TOE_DIFFERS_APPROVED: "search_findings.tab_events.type_values.toe_differs",
  };

  return eventType[field];
};

const castEventStatus: (field: string) => string = (field: string): string => {
  const eventStatus: Record<string, string> = {
    CREATED: "search_findings.tab_events.status_values.unsolve",
    SOLVED: "search_findings.tab_events.status_values.solve",
  };

  return eventStatus[field];
};

const formatDropdownField: (field: string) => string = (
  field: string
): string => {
  const translationParameters: Record<string, string> = {
    ACCEPTED: "search_findings.tab_description.treatment.accepted",
    ACCEPTED_UNDEFINED:
      "search_findings.tab_description.treatment.accepted_undefined",
    ANONYMOUS_INTERNET: "search_findings.tab_description.scenario.anon_inter",
    ANONYMOUS_INTRANET: "search_findings.tab_description.scenario.anon_intra",
    ANYONE_INTERNET: "search_findings.tab_description.actor.any_internet",
    ANYONE_WORKSTATION: "search_findings.tab_description.actor.any_station",
    ANY_CUSTOMER: "search_findings.tab_description.actor.any_customer",
    ANY_EMPLOYEE: "search_findings.tab_description.actor.any_employee",
    APPLICATIONS: "search_findings.tab_description.ambit.applications",
    AUTHORIZED_USER_EXTRANET:
      "search_findings.tab_description.scenario.auth_extra",
    AUTHORIZED_USER_INTERNET:
      "search_findings.tab_description.scenario.auth_inter",
    AUTHORIZED_USER_INTRANET:
      "search_findings.tab_description.scenario.auth_intra",
    DATABASES: "search_findings.tab_description.ambit.databases",
    INFRASTRUCTURE: "search_findings.tab_description.ambit.infra",
    IN_PROGRESS: "search_findings.tab_description.treatment.in_progress",
    NEW: "search_findings.tab_description.treatment.new",
    ONE_EMPLOYEE: "search_findings.tab_description.actor.one_employee",
    REJECTED: "search_findings.tab_description.treatment.rejected",
    SOME_CUSTOMERS: "search_findings.tab_description.actor.some_customer",
    SOME_EMPLOYEES: "search_findings.tab_description.actor.some_employee",
    SOURCE_CODE: "search_findings.tab_description.ambit.sourcecode",
    UNAUTHORIZED_USER_EXTRANET:
      "search_findings.tab_description.scenario.unauth_extra",
    UNAUTHORIZED_USER_INTERNET:
      "search_findings.tab_description.scenario.unauth_inter",
    UNAUTHORIZED_USER_INTRANET:
      "search_findings.tab_description.scenario.unauth_intra",
  };

  return translationParameters[field];
};

const formatTreatment: (treatment: string, findingState: string) => string = (
  treatment: string,
  findingState: string
): string => {
  const treatmentParameters: Record<string, string> = {
    "-": "-",
    ACCEPTED:
      findingState === "open"
        ? "search_findings.tab_description.treatment.accepted"
        : "-",
    ACCEPTED_UNDEFINED:
      findingState === "open"
        ? "search_findings.tab_description.treatment.accepted_undefined"
        : "-",
    "ACCEPTED_UNDEFINED pending":
      findingState === "open"
        ? translate.t(
            "search_findings.tab_description.treatment.accepted_undefined"
          ) +
          translate.t(
            "search_findings.tab_description.treatment.pending_approval"
          )
        : "-",
    "IN PROGRESS":
      findingState === "open"
        ? "search_findings.tab_description.treatment.in_progress"
        : "-",
    NEW:
      findingState === "open"
        ? "search_findings.tab_description.treatment.new"
        : "-",
  };
  const treatmentRes: string = translate.t(treatmentParameters[treatment]);

  return treatmentRes;
};

export {
  formatUserlist,
  formatLastLogin,
  castEventType,
  castEventStatus,
  formatDropdownField,
  formatTreatment,
};
