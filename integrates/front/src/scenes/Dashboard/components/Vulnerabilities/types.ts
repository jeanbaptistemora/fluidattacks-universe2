import type {
  ICustomFiltersProps,
  ICustomSearchProps,
} from "components/DataTableNext/types";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

interface IVulnRowAttr {
  commitHash?: string;
  currentState: "closed" | "open";
  currentStateCapitalized: "Closed" | "Open";
  cycles: string;
  efficacy: string;
  externalBugTrackingSystem?: string;
  hacker?: string;
  historicTreatment: IHistoricTreatment[];
  id: string;
  lastReattackDate?: string;
  lastReattackRequester: string;
  lastRequestedReattackDate?: string;
  remediated: boolean;
  reportDate: string;
  severity: string;
  specific: string;
  stream?: string;
  tag: string;
  treatment: string;
  treatmentChanges: number;
  treatmentDate: string;
  assigned: string;
  verification: string;
  vulnerabilityType: string;
  where: string;
  zeroRisk: string;
}

interface IUploadVulnerabilitiesResultAttr {
  uploadFile: {
    success: boolean;
  };
}

interface IDownloadVulnerabilitiesResultAttr {
  downloadVulnerabilityFile: {
    success: boolean;
    url: string;
  };
}

interface IVulnDataTypeAttr {
  currentState: "closed" | "open";
  externalBugTrackingSystem?: string;
  historicTreatment: IHistoricTreatment[];
  id: string;
  severity: string;
  specific: string;
  tag: string;
  assigned: string;
  where: string;
}

interface IVulnComponentProps {
  canDisplayHacker: boolean;
  customFilters?: ICustomFiltersProps;
  customSearch?: ICustomSearchProps;
  extraButtons: JSX.Element;
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
  externalBugTrackingSystem?: string;
  justification?: string;
  severity?: string;
  tag?: string;
  treatment: string;
  assigned?: string;
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
  IUpdateTreatmentVulnerabilityForm,
  IVulnDataTypeAttr,
  IVulnComponentProps,
};
