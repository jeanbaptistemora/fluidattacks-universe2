import type { FetchResult } from "@apollo/client";

interface IFindingMachineJob {
  createdAt: string | null;
  exitCode: number | null;
  exitReason: string | null;
  id: string;
  name: string;
  queue: string;
  rootNickname: string;
  startedAt: string | null;
  stoppedAt: string | null;
  status: string;
  vulnerabilities: IVulnerabilitiesDetails | null;
}

interface IVulnerabilitiesDetails {
  modified: number;
  open: number;
}

interface IExecution {
  createdAt: string | null;
  duration: number;
  jobId: string;
  name: string;
  priority: string;
  queue: string;
  status: string;
  startedAt: string | null;
  stoppedAt: string | null;
  rootId: string;
  rootNickname: string;
  vulnerabilities: IVulnerabilitiesDetails | null;
}
interface IGroupRoot {
  nickname: string;
  state: string;
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
    message: string;
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

interface IQueue {
  rootNicknames: string[];
  onClose: () => void;
  onSubmit: (
    rootNicknames: string[]
  ) => Promise<FetchResult<ISubmitMachineJobResult>>;
}

export {
  IExecution,
  IFindingMachineJob,
  IFindingMachineJobs,
  IGroupRoot,
  IQueue,
  ISubmitMachineJobResult,
  ITableRow,
};
