import type { IVulnDataAttr } from "../types";

interface ISubmittedTableProps {
  acceptanceVulns: IVulnDataAttr[];
  isOpenRejectLocationSelected: boolean;
  setAcceptanceVulns: (vulns: IVulnDataAttr[]) => void;
}

export type { ISubmittedTableProps };
