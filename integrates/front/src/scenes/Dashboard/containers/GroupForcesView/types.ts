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
  gitRepo: string;
  kind: string;
  log?: string;
  groupName?: string;
  status: string;
  strictness: string;
  vulnerabilities: IVulnerabilities;
}

interface IGetExecution {
  forcesExecutions: {
    executions: IExecution[];
  };
}

export {
  IExploitResult,
  IFoundVulnerabilities,
  IVulnerabilities,
  IExecution,
  IGetExecution,
};
