import type { IVulnDataAttr } from "../types";

interface IZeroRiskTableProps {
  acceptationVulns: IVulnDataAttr[];
  setAcceptationVulns: (vulns: IVulnDataAttr[]) => void;
}

export { IZeroRiskTableProps };
