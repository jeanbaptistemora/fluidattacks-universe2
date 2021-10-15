import type { IVulnDataAttr } from "../types";

interface IZeroRiskRejectionTableProps {
  acceptanceVulns: IVulnDataAttr[];
  isRejectZeroRiskSelected: boolean;
  setAcceptanceVulns: (vulns: IVulnDataAttr[]) => void;
}

export { IZeroRiskRejectionTableProps };
