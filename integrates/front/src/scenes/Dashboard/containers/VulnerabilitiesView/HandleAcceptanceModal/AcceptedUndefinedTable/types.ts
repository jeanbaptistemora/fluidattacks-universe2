import type { IVulnDataAttr } from "../types";

interface IAcceptedUndefinedTableProps {
  acceptationVulns: IVulnDataAttr[];
  isAcceptedUndefinedSelected: boolean;
  setAcceptationVulns: (vulns: IVulnDataAttr[]) => void;
}

export { IAcceptedUndefinedTableProps };
