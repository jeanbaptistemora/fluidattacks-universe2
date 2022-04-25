import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

interface IVulnTreatmentAttr {
  historicTreatment: IHistoricTreatment[];
}

interface IGetVulnTreatmentAttr {
  vulnerability: IVulnTreatmentAttr;
}

export type { IGetVulnTreatmentAttr };
