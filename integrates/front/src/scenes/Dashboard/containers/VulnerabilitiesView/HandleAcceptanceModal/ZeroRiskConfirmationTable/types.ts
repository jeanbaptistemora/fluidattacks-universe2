import type { IVulnDataAttr } from "../types";

interface IZeroRiskConfirmationTableProps {
  acceptanceVulns: IVulnDataAttr[];
  isConfirmZeroRiskSelected: boolean;
  setAcceptanceVulns: (vulns: IVulnDataAttr[]) => void;
}

export { IZeroRiskConfirmationTableProps };
