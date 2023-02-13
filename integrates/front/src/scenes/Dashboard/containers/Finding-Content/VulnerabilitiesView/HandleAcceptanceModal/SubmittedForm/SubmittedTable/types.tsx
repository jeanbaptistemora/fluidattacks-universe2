import type { IVulnDataAttr } from "../../types";

interface ISubmittedTableProps {
  acceptanceVulns: IVulnDataAttr[];
  isConfirmRejectVulnerabilitySelected: boolean;
  setAcceptanceVulns: (vulns: IVulnDataAttr[]) => void;
}

export type { ISubmittedTableProps };
