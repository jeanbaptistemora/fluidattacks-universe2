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

interface IFindingMachineJobs {
  finding: {
    machineJobs: IFindingMachineJob[];
  };
}

interface ITableRow {
  rootNickname: string;
  status: string;
}

export { IFindingMachineJob, IFindingMachineJobs, ITableRow };
