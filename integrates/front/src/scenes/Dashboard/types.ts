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
    phone: {
      callingCountryCode: string;
      nationalNumber: string;
    } | null;
    remember: boolean;
    sessionExpiration: string;
    tours: {
      newGroup: boolean;
      newRiskExposure: boolean;
      newRoot: boolean;
      welcome: boolean;
    };
    userEmail: string;
    userName: string;
  };
}

interface IOrganizationGroups {
  groups: IGroups[];
  name: string;
}

interface IGroups {
  name: string;
  permissions: string[];
  serviceAttributes: string[];
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

interface IGetMeVulnerabilitiesAssigned {
  me: {
    vulnerabilitiesAssigned: IVulnRowAttr[];
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

interface IRootIdAttr {
  id: string;
  nickname: string;
  state: "ACTIVE" | "INACTIVE";
}

interface IGroupRootIdsAttr {
  group: { name: string; roots: IRootIdAttr[] };
}

export type {
  IAddStakeholderAttr,
  IAssignedVulnerabilitiesContext,
  IGetMeVulnerabilitiesAssigned,
  IGetUserOrganizationsGroups,
  IGetVulnsGroups,
  IGroupRootIdsAttr,
  IGroups,
  IRootIdAttr,
  IOrganizationGroups,
  IUser,
};
