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

interface IHandleVulnerabilitiesAcceptationModalProps {
  findingId: string;
  groupName: string;
  vulns: IVulnerabilitiesAttr[];
  handleCloseModal: () => void;
  refetchData: () => void;
}

interface IHandleVulnerabilitiesAcceptationModalFormProps {
  acceptationVulns: IVulnDataAttr[];
  acceptedVulns: IVulnDataAttr[];
  rejectedVulns: IVulnDataAttr[];
  hasAcceptedVulns: boolean;
  hasRejectedVulns: boolean;
  handlingAcceptation: boolean;
  confirmingZeroRisk: boolean;
  rejectingZeroRisk: boolean;
  setAcceptationVulns: React.Dispatch<React.SetStateAction<IVulnDataAttr[]>>;
  handleCloseModal: () => void;
  vulns: IVulnerabilitiesAttr[];
}

interface IHandleVulnerabilitiesAcceptationResultAttr {
  handleVulnerabilitiesAcceptation: {
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
  IHandleVulnerabilitiesAcceptationModalFormProps,
  IHandleVulnerabilitiesAcceptationModalProps,
  IHandleVulnerabilitiesAcceptationResultAttr,
  IRejectZeroRiskVulnResultAttr,
  IVulnDataAttr,
};
