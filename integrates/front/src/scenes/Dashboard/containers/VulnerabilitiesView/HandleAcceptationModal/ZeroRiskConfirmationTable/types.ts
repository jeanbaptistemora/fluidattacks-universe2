import type { IVulnDataAttr } from "../types";

interface IZeroRiskConfirmationTableProps {
  acceptationVulns: IVulnDataAttr[];
  isConfirmZeroRiskSelected: boolean;
  setAcceptationVulns: (vulns: IVulnDataAttr[]) => void;
}

export { IZeroRiskConfirmationTableProps };
