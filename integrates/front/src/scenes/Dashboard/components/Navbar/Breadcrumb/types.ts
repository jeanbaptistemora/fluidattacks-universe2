import type { IVulnRowAttr } from "../../Vulnerabilities/types";

interface IUserOrgs {
  me: {
    organizations: { name: string }[];
    userEmail: string;
  };
}

interface IFindingTitle {
  finding: {
    title: string;
  };
}

interface IOrganizationGroups {
  groups: {
    name: string;
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

export {
  IFindingTitle,
  IGetUserOrganizationsGroups,
  IGetVulnsGroups,
  IOrganizationGroups,
  IUserOrgs,
};
