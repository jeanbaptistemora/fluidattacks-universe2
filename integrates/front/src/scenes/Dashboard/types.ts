import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

interface IAddStakeholderAttr {
  addStakeholder: {
    email: string;
    success: boolean;
  };
}

interface IUser {
  me: {
    isConcurrentSession: boolean;
    permissions: string[];
    remember: boolean;
    sessionExpiration: string;
    userEmail: string;
    userName: string;
  };
}

interface IOrganizationGroups {
  groups: {
    name: string;
    permissions: string[];
  }[];
  name: string;
}

interface IGetVulnsGroups {
  group: {
    vulnerabilitiesAssigned: IVulnRowAttr[];
    name: string;
  };
}

interface IGetUserOrganizationsGroups {
  me: {
    organizations: IOrganizationGroups[];
    userEmail: string;
  };
}

interface IAssignedVulnerabilitiesContext
  extends Array<
    IGetVulnsGroups[] | React.Dispatch<React.SetStateAction<IGetVulnsGroups[]>>
  > {
  0: IGetVulnsGroups[];
  1: React.Dispatch<React.SetStateAction<IGetVulnsGroups[]>>;
}

export {
  IAddStakeholderAttr,
  IAssignedVulnerabilitiesContext,
  IGetUserOrganizationsGroups,
  IGetVulnsGroups,
  IOrganizationGroups,
  IUser,
};
