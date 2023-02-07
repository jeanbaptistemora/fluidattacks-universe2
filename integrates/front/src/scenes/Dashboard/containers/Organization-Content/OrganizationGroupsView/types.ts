interface IGroupData {
  description: string;
  eventFormat: string;
  events: {
    eventStatus: string;
  }[];
  hasMachine: boolean;
  hasSquad: boolean;
  machine: string;
  managed: "MANAGED" | "NOT_MANAGED" | "TRIAL" | "UNDER_REVIEW";
  name: string;
  openFindings: number;
  plan: string;
  service: string;
  squad: string;
  status: string;
  subscription: string;
  userRole: string;
  vulnerabilities: string;
}

interface IOrganizationGroupsProps {
  organizationId: string;
}

interface IGetOrganizationGroups {
  organization: {
    name: string;
    coveredAuthors: number;
    coveredRepositories: number;
    missedAuthors: number;
    missedRepositories: number;
    groups: IGroupData[];
    trial: ITrialData | null;
  };
}

interface ITrialData {
  completed: boolean;
  extensionDate: string;
  extensionDays: number;
  startDate: string;
  state: "EXTENDED_END" | "EXTENDED" | "TRIAL_ENDED" | "TRIAL";
}

export type {
  IGroupData,
  IOrganizationGroupsProps,
  IGetOrganizationGroups,
  ITrialData,
};
