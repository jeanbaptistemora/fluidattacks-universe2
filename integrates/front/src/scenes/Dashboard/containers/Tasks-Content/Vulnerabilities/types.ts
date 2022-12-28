import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

interface ITasksVulnerabilities {
  setUserRole: (userRole: string | undefined) => void;
}

interface IAction {
  action: string;
}
interface IGroupAction {
  groupName: string;
  actions: IAction[];
}

interface IGetMeVulnerabilitiesAssigned {
  me: {
    vulnerabilitiesAssigned: IVulnRowAttr[];
    userEmail: string;
  };
}

export type {
  IAction,
  IGetMeVulnerabilitiesAssigned,
  IGroupAction,
  ITasksVulnerabilities,
};
