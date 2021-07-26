interface IFindingMachineJob {
  createdAt: string | null;
  exitCode: string | null;
  exitReason: string | null;
  id: string;
  name: string;
  queue: string;
  rootNickname: string;
  startedAt: string | null;
  stoppedAt: string | null;
  status: string;
}

interface IGroupRoot {
  nickname: string;
}

interface IFindingMachineJobs {
  finding: {
    machineJobs: IFindingMachineJob[];
  };
  group: {
    roots: IGroupRoot[];
  };
}

interface ISubmitMachineJobResult {
  submitMachineJob: {
    success: boolean;
  };
}

interface ITableRow {
  duration: number;
  priority: string;
  rootNickname: string;
  startedAt: number;
  status: string;
}

export {
  IFindingMachineJob,
  IFindingMachineJobs,
  IGroupRoot,
  ISubmitMachineJobResult,
  ITableRow,
};
