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

interface IFilterTodosSet {
  reportDateRange?: { max: string; min: string };
  tag: string;
  treatment: string;
  treatmentCurrentStatus: string;
  verification?: string;
}

interface IGetMeVulnerabilitiesAssigned {
  me: {
    vulnerabilitiesAssigned: IVulnRowAttr[];
    userEmail: string;
  };
}

export type {
  IAction,
  IFilterTodosSet,
  IGetMeVulnerabilitiesAssigned,
  IGroupAction,
  ITasksVulnerabilities,
};
