import type { IHistoricTreatment } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";

interface IVulnTreatmentAttr {
  historicTreatment: IHistoricTreatment[];
}

interface IGetVulnTreatmentAttr {
  vulnerability: IVulnTreatmentAttr;
}

export type { IGetVulnTreatmentAttr };
