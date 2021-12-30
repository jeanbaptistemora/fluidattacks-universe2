import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

interface IVulnInfoAttr {
  commitHash: string | null;
  cycles: string;
  efficacy: string;
  hacker?: string;
  historicTreatment: IHistoricTreatment[];
  lastReattackRequester: string;
  lastRequestedReattackDate: string | null;
}

interface IGetVulnAdditionalInfoAttr {
  vulnerability: IVulnInfoAttr;
}

export { IGetVulnAdditionalInfoAttr };
