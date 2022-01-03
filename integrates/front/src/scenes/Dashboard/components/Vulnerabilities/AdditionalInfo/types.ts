import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

interface IVulnInfoAttr {
  commitHash: string | null;
  cycles: string;
  efficacy: string;
  hacker?: string;
  historicTreatment: IHistoricTreatment[];
  lastReattackRequester: string;
  lastRequestedReattackDate: string | null;
  reportDate: string;
  severity: string | null;
  stream: string | null;
  treatmentAssigned: string | null;
  treatmentJustification: string | null;
  vulnerabilityType: string;
}

interface IGetVulnAdditionalInfoAttr {
  vulnerability: IVulnInfoAttr;
}

export { IGetVulnAdditionalInfoAttr };
