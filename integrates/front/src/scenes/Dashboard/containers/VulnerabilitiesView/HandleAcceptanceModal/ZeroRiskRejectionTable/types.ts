import type { IVulnDataAttr } from "../types";

interface IZeroRiskRejectionTableProps {
  acceptationVulns: IVulnDataAttr[];
  isRejectZeroRiskSelected: boolean;
  setAcceptationVulns: (vulns: IVulnDataAttr[]) => void;
}

export { IZeroRiskRejectionTableProps };
