import type { IVulnerabilitiesAttr } from "../types";

interface IVulnDataAttr {
  acceptation: "" | "APPROVED" | "REJECTED";
  id: string;
  specific: string;
  where: string;
}

interface IFormValues {
  justification: string;
  treatment: string;
}

interface IHandleVulnerabilitiesAcceptanceModalProps {
  findingId: string;
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
  handlingAcceptation: boolean;
  confirmingZeroRisk: boolean;
  rejectingZeroRisk: boolean;
  setAcceptationVulns: React.Dispatch<React.SetStateAction<IVulnDataAttr[]>>;
  handleCloseModal: () => void;
  vulns: IVulnerabilitiesAttr[];
}

interface IHandleVulnerabilitiesAcceptanceResultAttr {
  handleVulnerabilitiesAcceptance: {
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

export {
  IConfirmVulnZeroRiskResultAttr,
  IFormValues,
  IHandleVulnerabilitiesAcceptanceModalFormProps,
  IHandleVulnerabilitiesAcceptanceModalProps,
  IHandleVulnerabilitiesAcceptanceResultAttr,
  IRejectZeroRiskVulnResultAttr,
  IVulnDataAttr,
};
