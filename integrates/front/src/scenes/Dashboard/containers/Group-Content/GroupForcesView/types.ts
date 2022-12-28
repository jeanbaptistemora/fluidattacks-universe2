interface IExploitResult {
  exploitability: number;
  kind: string;
  state: string;
  where: string;
  who: string;
}

interface IFoundVulnerabilities {
  accepted: number;
  closed: number;
  open: number;
  total: number;
}

interface IVulnerabilities {
  accepted: IExploitResult[];
  closed: IExploitResult[];
  numOfAcceptedVulnerabilities: number;
  numOfClosedVulnerabilities: number;
  numOfOpenVulnerabilities: number;
  open: IExploitResult[];
}

interface IExecution {
  date: string;
  executionId: string;
  exitCode: string;
  foundVulnerabilities: IFoundVulnerabilities;
  gracePeriod: number;
  gitRepo: string;
  kind: string;
  log?: string;
  groupName?: string;
  status: string;
  strictness: string;
  severityThreshold: number;
  vulnerabilities: IVulnerabilities | null;
}

interface IGroupExecutions {
  group: {
    executionsConnections: {
      edges: { node: IExecution }[];
      pageInfo: {
        endCursor: string;
        hasNextPage: boolean;
      };
      total: number | undefined;
    };
    name: string;
  };
}

interface IGetForcesExecution {
  forcesExecution: {
    groupName: string;
    log: string;
    vulnerabilities: IVulnerabilities | null;
  };
}

export type {
  IExploitResult,
  IFoundVulnerabilities,
  IVulnerabilities,
  IExecution,
  IGroupExecutions,
  IGetForcesExecution,
};
