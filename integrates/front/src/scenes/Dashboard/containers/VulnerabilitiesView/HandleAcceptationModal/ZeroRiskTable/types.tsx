import type { IVulnDataAttr } from "../types";

interface IZeroRiskTableProps {
  acceptationVulns: IVulnDataAttr[];
  isConfirmRejectZeroRiskSelected: boolean;
  setAcceptationVulns: (vulns: IVulnDataAttr[]) => void;
}

export { IZeroRiskTableProps };
