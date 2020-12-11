import { IVulnDataType } from "scenes/Dashboard/components/Vulnerabilities/types";

interface IUpdateTreatmentModal {
  findingId: string;
  projectName?: string;
  vulnerabilities: IVulnDataType[];
  vulnerabilitiesChunk: number;
  handleClearSelected(): void;
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
  updateTreatmentVuln?: {
    success: boolean;
  };
  updateVulnsTreatment?: {
    success: boolean;
  };
}

interface IRequestZeroRiskVulnResult {
  requestZeroRiskVuln: {
    success: boolean;
  };
}

export {
  IDeleteTagAttr,
  IDeleteTagResult,
  IRequestZeroRiskVulnResult,
  IUpdateTreatmentModal,
  IUpdateVulnDescriptionResult,
};
