interface IMachineExecution {
  createdAt: string;
  findingsExecuted: IFindingExecuted[];
  jobId: string;
  name: string;
  queue: string;
  startedAt: string;
  stoppedAt: string;
}
interface IExecution {
  jobId: string;
  createdAt: string;
  startedAt: string;
  stoppedAt: string;
  duration: string;
  findingsExecuted: IFindingExecuted[];
  name: string;
  queue: string;
  rootId: string;
  rootNickname: string;
}

interface IRoot {
  id: string;
  machineExecutions: IMachineExecution[];
  nickname: string;
}

interface IFindingExecuted {
  finding: string;
  modified: number;
  open: number;
}

interface IGetExecutions {
  group: {
    name: string;
    roots: IRoot[];
  };
}

export {
  IGetExecutions,
  IExecution,
  IMachineExecution,
  IRoot,
  IFindingExecuted,
};
