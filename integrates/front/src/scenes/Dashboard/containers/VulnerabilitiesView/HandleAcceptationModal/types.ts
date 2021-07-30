import type { IVulnerabilitiesAttr } from "../types";

interface IVulnDataAttr {
  acceptation: "" | "APPROVED" | "REJECTED";
  id: string;
  specific: string;
  where: string;
}

interface IHandleVulnerabilitiesAcceptationModalProps {
  findingId: string;
  groupName: string;
  vulns: IVulnerabilitiesAttr[];
  handleCloseModal: () => void;
  refetchData: () => void;
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
  IHandleVulnerabilitiesAcceptationModalProps,
  IHandleVulnerabilitiesAcceptationResultAttr,
  IRejectZeroRiskVulnResultAttr,
  IVulnDataAttr,
};
