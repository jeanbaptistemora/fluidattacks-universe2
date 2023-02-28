interface IGetMeVulnerabilitiesAssignedIds {
  me: {
    vulnerabilitiesAssigned: { id: string }[];
    userEmail: string;
  };
}

interface INavbarProps {
  allAssigned: number;
  meVulnerabilitiesAssignedIds: IGetMeVulnerabilitiesAssignedIds | undefined;
  undefinedOrEmpty: boolean;
  userRole: string | undefined;
}

export type { IGetMeVulnerabilitiesAssignedIds, INavbarProps };
