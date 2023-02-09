import type { IVulnDataAttr } from "../types";

interface ISubmittedTableProps {
  acceptanceVulns: IVulnDataAttr[];
  isConfirmRejectLocationSelected: boolean;
  setAcceptanceVulns: (vulns: IVulnDataAttr[]) => void;
}

export type { ISubmittedTableProps };
