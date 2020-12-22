import type { IVulnerabilities } from "../types";

interface IVulnDataAttr {
  acceptation: "APPROVED" | "REJECTED" | "";
  id: string;
  specific: string;
  where: string;
}

interface IHandleVulnsAcceptationModalProps {
  findingId: string;
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

export {
  IConfirmZeroRiskVulnResultAttr,
  IHandleVulnsAcceptationModalProps,
  IHandleVulnsAcceptationResultAttr,
  IVulnDataAttr,
};
