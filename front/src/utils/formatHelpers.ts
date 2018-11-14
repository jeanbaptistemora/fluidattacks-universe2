import { IProjectUsersViewProps } from "../scenes/Dashboard/components/ProjectUsersView";
import translate from "./translations/translate";

export const formatUserlist:
((arg1: IProjectUsersViewProps["userList"]) => IProjectUsersViewProps["userList"]) =
  (userList: IProjectUsersViewProps["userList"]): IProjectUsersViewProps["userList"] => {
  for (const user of userList) {
    user.role = translate.t(`search_findings.tab_users.${user.role}`);
    const lastLoginDate: number[] = JSON.parse(user.lastLogin);
    let DAYS_IN_MONTH: number;
    DAYS_IN_MONTH = 30;

    if (lastLoginDate[0] >= DAYS_IN_MONTH) {
      const ROUNDED_MONTH: number = Math.round(lastLoginDate[0] / DAYS_IN_MONTH);
      user.lastLogin = translate.t("search_findings.tab_users.months_ago", {count: ROUNDED_MONTH});
    } else if (lastLoginDate[0] > 0 && lastLoginDate[0] < DAYS_IN_MONTH) {
      user.lastLogin = translate.t("search_findings.tab_users.days_ago", {count: lastLoginDate[0]});
    } else if (lastLoginDate[0] === -1) {
      user.lastLogin = "-";
      user.firstLogin = "-";
    } else {
      let SECONDS_IN_HOUR: number;
      SECONDS_IN_HOUR = 3600;
      const ROUNDED_HOUR: number = Math.round(lastLoginDate[1] / SECONDS_IN_HOUR);
      let SECONDS_IN_MINUTES: number;
      SECONDS_IN_MINUTES = 60;
      const ROUNDED_MINUTES: number = Math.round(lastLoginDate[1] / SECONDS_IN_MINUTES);
      user.lastLogin = ROUNDED_HOUR >= 1 && ROUNDED_MINUTES >= SECONDS_IN_MINUTES
      ? translate.t("search_findings.tab_users.hours_ago", {count: ROUNDED_HOUR})
      : translate.t("search_findings.tab_users.minutes_ago", {count: ROUNDED_MINUTES});
    }
  }

  return userList;
};
