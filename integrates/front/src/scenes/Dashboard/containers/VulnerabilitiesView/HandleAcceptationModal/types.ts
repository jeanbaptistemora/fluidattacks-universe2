import type { IVulnerabilities } from "../types";

interface IVulnDataAttr {
  acceptation: "APPROVED" | "REJECTED" | "";
  id: string;
  specific: string;
  where: string;
}

interface IHandleVulnsAcceptationModalProps {
  findingId: string;
  groupName: string;
  vulns: IVulnerabilities[];
  handleCloseModal: () => void;
  refetchData: () => void;
}

interface IHandleVulnsAcceptationResultAttr {
  handleVulnsAcceptation: {
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
  IHandleVulnsAcceptationModalProps,
  IHandleVulnsAcceptationResultAttr,
  IRejectZeroRiskVulnResultAttr,
  IVulnDataAttr,
};
