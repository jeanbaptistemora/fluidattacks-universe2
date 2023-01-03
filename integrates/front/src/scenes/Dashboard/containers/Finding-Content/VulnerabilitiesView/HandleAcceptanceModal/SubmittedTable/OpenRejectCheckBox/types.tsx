import type { IVulnDataAttr } from "../../types";

interface IOpenRejectCheckBoxProps {
  approveFunction: (vulnerabilityRow: IVulnDataAttr) => void;
  deleteFunction: (vulnerabilityRow: IVulnDataAttr) => void;
  vulnerabilityRow: IVulnDataAttr;
}

export type { IOpenRejectCheckBoxProps };
