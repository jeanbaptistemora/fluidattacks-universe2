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
    coveredCommits: number;
    coveredRepositories: number;
    missedCommits: number;
    missedRepositories: number;
    groups: IGroupData[];
  };
}

export type { IGroupData, IOrganizationGroupsProps, IGetOrganizationGroups };
