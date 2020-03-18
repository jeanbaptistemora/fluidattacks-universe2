export interface IForcesIndicatorsViewBaseProps {
  projectName: string;
}

export interface IForcesVulnerabilities {
  numOfVulnerabilitiesInAcceptedExploits: number;
  numOfVulnerabilitiesInExploits: number;
  numOfVulnerabilitiesInMockedExploits: number;
}

export interface IForcesExecution {
  strictness: string;
  vulnerabilities: IForcesVulnerabilities;
}

export interface IForcesIndicatorsProps {
  forcesExecutions: {
    executions: IForcesExecution[];
  };
  project: {
    hasForces: boolean;
  };
}
