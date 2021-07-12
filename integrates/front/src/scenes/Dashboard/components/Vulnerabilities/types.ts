import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

interface IVulnRowAttr {
  analyst?: string;
  commitHash: string;
  currentState: "closed" | "open";
  currentStateCapitalized: "Closed" | "Open";
  cycles: string;
  efficacy: string;
  externalBts: string;
  historicTreatment: IHistoricTreatment[];
  id: string;
  lastReattackDate: string;
  lastReattackRequester: string;
  lastRequestedReattackDate: string;
  remediated: boolean;
  reportDate: string;
  severity: string;
  specific: string;
  stream: string;
  tag: string;
  treatment: string;
  treatmentChanges: number;
  treatmentDate: string;
  treatmentManager: string;
  verification: string;
  vulnType: string;
  where: string;
  zeroRisk: string;
}

interface IUploadVulnerabilitiesResultAttr {
  uploadFile: {
    success: boolean;
  };
}

interface IDownloadVulnerabilitiesResultAttr {
  downloadVulnFile: {
    success: boolean;
    url: string;
  };
}

interface IUpdateTreatmentVulnAttr {
  acceptanceDate: string;
  externalBts: string;
  findingId: string;
  justification: string;
  severity?: number;
  tag?: string;
  treatment: string;
  treatmentManager: string;
  vulnerabilities: string[];
}

interface IVulnDataTypeAttr {
  currentState: "closed" | "open";
  externalBts: string;
  historicTreatment: IHistoricTreatment[];
  id: string;
  severity: string;
  specific: string;
  tag: string;
  treatmentManager: string;
  where: string;
}

interface IVulnComponentProps {
  canDisplayAnalyst: boolean;
  findingId: string;
  findingState: "closed" | "open";
  groupName: string;
  isFindingReleased: boolean;
  isEditing: boolean;
  isRequestingReattack: boolean;
  isVerifyingRequest: boolean;
  vulnerabilities: IVulnRowAttr[];
  onVulnSelect: (
    vulnerabilities: IVulnRowAttr[],
    clearSelected: () => void
  ) => void;
}

interface IUpdateTreatmentVulnerabilityForm {
  acceptanceDate?: string;
  externalBts: string;
  justification?: string;
  severity?: string;
  tag?: string;
  treatment: string;
  treatmentManager?: string;
}

interface IVulnerabilityModalValues
  extends Array<
    | IUpdateTreatmentVulnerabilityForm
    | React.Dispatch<React.SetStateAction<IUpdateTreatmentVulnerabilityForm>>
  > {
  0: IUpdateTreatmentVulnerabilityForm;
  1: React.Dispatch<React.SetStateAction<IUpdateTreatmentVulnerabilityForm>>;
}

export {
  IVulnRowAttr,
  IUploadVulnerabilitiesResultAttr,
  IDownloadVulnerabilitiesResultAttr,
  IVulnerabilityModalValues,
  IUpdateTreatmentVulnAttr,
  IUpdateTreatmentVulnerabilityForm,
  IVulnDataTypeAttr,
  IVulnComponentProps,
};
