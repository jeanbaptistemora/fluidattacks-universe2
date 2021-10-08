import type { IVulnDataAttr } from "../types";

interface IZeroRiskTableProps {
  acceptanceVulns: IVulnDataAttr[];
  isConfirmRejectZeroRiskSelected: boolean;
  setAcceptanceVulns: (vulns: IVulnDataAttr[]) => void;
}

export { IZeroRiskTableProps };
