import type { IVulnerabilitiesAttr } from "../types";

interface IVulnDataAttr {
  acceptance: "" | "APPROVED" | "REJECTED";
  findingId: string;
  id: string;
  specific: string;
  where: string;
}

interface IFormValues {
  justification: string;
}

interface IHandleVulnerabilitiesAcceptanceModalProps {
  findingId?: string;
  groupName: string;
  vulns: IVulnerabilitiesAttr[];
  handleCloseModal: () => void;
  refetchData: () => void;
}

interface IHandleVulnerabilitiesAcceptanceModalFormProps {
  acceptanceVulnerabilities: IVulnDataAttr[];
  acceptedVulnerabilities: IVulnDataAttr[];
  rejectedVulnerabilities: IVulnDataAttr[];
  hasAcceptedVulns: boolean;
  hasRejectedVulns: boolean;
  handlingAcceptance: boolean;
  confirmingZeroRisk: boolean;
  rejectingZeroRisk: boolean;
  setAcceptanceVulns: React.Dispatch<React.SetStateAction<IVulnDataAttr[]>>;
  treatment: string;
  handleCloseModal: () => void;
  vulns: IVulnerabilitiesAttr[];
}

interface IHandleVulnerabilitiesAcceptanceResultAttr {
  handleVulnerabilitiesAcceptance: {
    success: boolean;
  };
}

interface IConfirmVulnerabilitiesResultAttr {
  confirmVulnerabilities: {
    success: boolean;
  };
}

interface IConfirmVulnZeroRiskResultAttr {
  confirmVulnerabilitiesZeroRisk: {
    success: boolean;
  };
}

interface IRejectZeroRiskVulnResultAttr {
  rejectVulnerabilitiesZeroRisk: {
    success: boolean;
  };
}

export type {
  IConfirmVulnerabilitiesResultAttr,
  IConfirmVulnZeroRiskResultAttr,
  IFormValues,
  IHandleVulnerabilitiesAcceptanceModalFormProps,
  IHandleVulnerabilitiesAcceptanceModalProps,
  IHandleVulnerabilitiesAcceptanceResultAttr,
  IRejectZeroRiskVulnResultAttr,
  IVulnDataAttr,
};
