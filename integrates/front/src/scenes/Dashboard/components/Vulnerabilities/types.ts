import type {
  ICustomFiltersProps,
  ICustomSearchProps,
} from "components/DataTableNext/types";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

interface IVulnRowAttr {
  currentState: "closed" | "open";
  currentStateCapitalized: "Closed" | "Open";
  externalBugTrackingSystem: string | null;
  findingId: string;
  groupName: string;
  historicTreatment: IHistoricTreatment[];
  id: string;
  lastTreatmentDate: string;
  lastVerificationDate: string | null;
  remediated: boolean;
  reportDate: string;
  severity: string | null;
  specific: string;
  stream: string | null;
  tag: string;
  treatment: string;
  treatmentDate: string;
  treatmentAcceptanceDate: string | null;
  treatmentAcceptanceStatus: string | null;
  treatmentAssigned: string | null;
  treatmentJustification: string | null;
  assigned: string;
  verification: string | null;
  vulnerabilityType: string;
  where: string;
  zeroRisk: string | null;
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
  externalBugTrackingSystem: string | null;
  groupName: string;
  historicTreatment: IHistoricTreatment[];
  id: string;
  severity: string | null;
  specific: string;
  tag: string;
  assigned: string;
  where: string;
}

interface IVulnComponentProps {
  canDisplayHacker: boolean;
  clearFiltersButton?: () => void;
  changePermissions?: (groupName: string) => void;
  customFilters?: ICustomFiltersProps;
  customSearch?: ICustomSearchProps;
  extraButtons: JSX.Element;
  findingState: "closed" | "open";
  hideSelectVulnerability?: boolean;
  isFindingReleased: boolean;
  isEditing: boolean;
  isRequestingReattack: boolean;
  isVerifyingRequest: boolean;
  nonValidOnReattackVulnerabilities?: IVulnRowAttr[];
  vulnerabilities: IVulnRowAttr[];
  onVulnSelect: (
    vulnerabilities: IVulnRowAttr[],
    clearSelected: () => void
  ) => void;
}

interface IUpdateTreatmentVulnerabilityForm {
  acceptanceDate?: string;
  externalBugTrackingSystem: string | null;
  justification?: string;
  severity: string | null;
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
