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

interface IOrganizationGroups {
  groups: {
    name: string;
    permissions: string[];
    serviceAttributes: string[];
  }[];
  name: string;
}

interface IGetUserOrganizationsGroups {
  me: {
    organizations: IOrganizationGroups[];
    userEmail: string;
  };
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
  IGetUserOrganizationsGroups,
  IGroupAction,
  ITasksVulnerabilities,
};
