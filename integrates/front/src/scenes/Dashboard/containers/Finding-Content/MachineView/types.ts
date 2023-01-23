import type { FetchResult } from "@apollo/client";

interface IGroupRoot {
  nickname: string;
  state: string;
}

interface IFindingMachineJobs {
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

interface IQueue {
  rootNicknames: string[];
  onClose: () => void;
  onSubmit: (
    rootNicknames: string[]
  ) => Promise<FetchResult<ISubmitMachineJobResult>>;
}

export type {
  IFindingMachineJobs,
  IGroupRoot,
  IQueue,
  ISubmitMachineJobResult,
};
