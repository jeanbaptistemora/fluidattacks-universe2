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

interface IConfirmZeroRiskVulnResultAttr {
  confirmZeroRiskVuln: {
    success: boolean;
  };
}

interface IRejectZeroRiskVulnResultAttr {
  rejectZeroRiskVuln: {
    success: boolean;
  };
}

export {
  IConfirmZeroRiskVulnResultAttr,
  IHandleVulnerabilitiesAcceptationModalProps,
  IHandleVulnerabilitiesAcceptationResultAttr,
  IRejectZeroRiskVulnResultAttr,
  IVulnDataAttr,
};
