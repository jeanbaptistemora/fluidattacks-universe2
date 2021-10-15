import type { IVulnDataAttr } from "../types";

interface IAcceptedUndefinedTableProps {
  acceptanceVulns: IVulnDataAttr[];
  isAcceptedUndefinedSelected: boolean;
  setAcceptanceVulns: (vulns: IVulnDataAttr[]) => void;
}

export { IAcceptedUndefinedTableProps };
