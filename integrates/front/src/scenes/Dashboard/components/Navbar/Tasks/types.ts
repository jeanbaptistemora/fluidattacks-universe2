interface IGetMeVulnerabilitiesAssignedIds {
  me: {
    vulnerabilitiesAssigned: { id: string }[];
    userEmail: string;
  };
}

export type { IGetMeVulnerabilitiesAssignedIds };
