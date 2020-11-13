import { IVulnDataType } from "scenes/Dashboard/components/Vulnerabilities/types";
import { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

interface IUpdateTreatmentModal {
  findingId: string;
  lastTreatment?: IHistoricTreatment;
  projectName?: string;
  vulnerabilities: IVulnDataType[];
  handleCloseModal(): void;
}

interface IDeleteTagAttr {
  findingId: string;
  tag?: string;
  vulnerabilities: string[];
}

interface IDeleteTagResult {
  deleteTags: {
    success: boolean;
  };
}

interface IUpdateVulnDescriptionResult {
  updateTreatmentVuln: {
    success: boolean;
  };
}

export {
  IDeleteTagAttr,
  IDeleteTagResult,
  IUpdateTreatmentModal,
  IUpdateVulnDescriptionResult,
};
