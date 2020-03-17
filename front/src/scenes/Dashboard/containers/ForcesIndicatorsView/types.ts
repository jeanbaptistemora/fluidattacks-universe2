export interface IForcesIndicatorsViewBaseProps {
  projectName: string;
}

export interface IForcesExecution {
  strictness: string;
}

export interface IForcesIndicatorsProps {
  forcesExecutions: {
    executions: [IForcesExecution];
  };
  project: {
    hasForces: boolean;
  };
}
