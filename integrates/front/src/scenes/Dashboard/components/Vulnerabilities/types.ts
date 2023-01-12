import type { ColumnDef, ColumnFiltersState } from "@tanstack/react-table";
import type { Dispatch, SetStateAction } from "react";

import type { IHistoricTreatment } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";
import type {
  IRequirementData,
  IVulnData,
} from "scenes/Dashboard/containers/Group-Content/GroupDraftsView/types";
import type { IFinding } from "scenes/Dashboard/containers/Group-Content/GroupVulnerabilitiesView/types";

interface IVulnRowAttr {
  externalBugTrackingSystem: string | null;
  findingId: string;
  groupName: string;
  organizationName: string | undefined;
  historicTreatment: IHistoricTreatment[];
  id: string;
  lastTreatmentDate: string;
  lastVerificationDate: string | null;
  remediated: boolean;
  reportDate: string;
  rootNickname: string | null;
  severity: string | null;
  snippet: ISnippet | null;
  source: string;
  specific: string;
  state: "REJECTED" | "SAFE" | "SUBMITTED" | "VULNERABLE";
  stream: string | null;
  tag: string;
  treatmentDate: string;
  treatmentAcceptanceDate: string | null;
  treatmentAcceptanceStatus: string | null;
  treatmentAssigned: string | null;
  treatmentJustification: string | null;
  treatmentStatus: string;
  treatmentUser: string | null;
  assigned: string;
  verification: string | null;
  vulnerabilityType: string;
  where: string;
  zeroRisk: string | null;
  finding?: IFinding;
  requirements?: string[];
}

interface ISnippet {
  content: string;
  offset: number;
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
  externalBugTrackingSystem: string | null;
  findingId: string;
  groupName: string;
  historicTreatment: IHistoricTreatment[];
  id: string;
  severity: string | null;
  source: string;
  specific: string;
  state: "REJECTED" | "SAFE" | "SUBMITTED" | "VULNERABLE";
  tag: string;
  assigned: string;
  where: string;
}

interface IVulnComponentProps {
  clearFiltersButton?: () => void;
  changePermissions?: (groupName: string) => void;
  columnFilterSetter?: Dispatch<SetStateAction<ColumnFiltersState>>;
  columnFilterState?: ColumnFiltersState;
  columnToggle?: boolean;
  columns: ColumnDef<IVulnRowAttr>[];
  enableColumnFilters?: boolean;
  extraButtons?: JSX.Element;
  filters?: JSX.Element;
  findingState?: "SAFE" | "VULNERABLE";
  hideSelectVulnerability?: boolean;
  isFindingReleased?: boolean;
  isEditing: boolean;
  isRequestingReattack: boolean;
  isVerifyingRequest: boolean;
  refetchData: () => void;
  size?: number;
  nonValidOnReattackVulnerabilities?: IVulnRowAttr[];
  vulnerabilities: IVulnRowAttr[];
  onNextPage?: () => Promise<void>;
  onSearch?: (search: string) => void;
  onVulnSelect?: (
    vulnerabilities: IVulnRowAttr[],
    clearSelected: () => void
  ) => void;
  vulnData?: Record<string, IVulnData>;
  requirementData?: Record<string, IRequirementData>;
}

interface IUpdateVulnerabilityForm {
  acceptanceDate?: string;
  externalBugTrackingSystem: string | null;
  justification?: string;
  severity: string | null;
  source?: string;
  tag?: string;
  treatment: string;
  assigned?: string;
}

interface IVulnerabilityModalValues
  extends Array<
    | IUpdateVulnerabilityForm
    | React.Dispatch<React.SetStateAction<IUpdateVulnerabilityForm>>
  > {
  0: IUpdateVulnerabilityForm;
  1: React.Dispatch<React.SetStateAction<IUpdateVulnerabilityForm>>;
}

export type {
  IVulnRowAttr,
  IUploadVulnerabilitiesResultAttr,
  IDownloadVulnerabilitiesResultAttr,
  IVulnerabilityModalValues,
  IUpdateVulnerabilityForm,
  IVulnDataTypeAttr,
  IVulnComponentProps,
};
