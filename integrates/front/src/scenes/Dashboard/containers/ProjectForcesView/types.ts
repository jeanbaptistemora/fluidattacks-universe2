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
  // eslint-disable-next-line camelcase -- API related
  execution_id: string;
  exitCode: string;
  foundVulnerabilities: IFoundVulnerabilities;
  gitRepo: string;
  kind: string;
  log?: string;
  projectName?: string;
  status: string;
  strictness: string;
  vulnerabilities: IVulnerabilities;
}

export { IExploitResult, IFoundVulnerabilities, IVulnerabilities, IExecution };
