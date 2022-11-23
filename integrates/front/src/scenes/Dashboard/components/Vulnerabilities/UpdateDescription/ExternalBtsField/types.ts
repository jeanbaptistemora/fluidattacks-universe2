import type { IVulnDataTypeAttr } from "../../types";

interface IExternalBtsFieldProps {
  hasNewVulnSelected: boolean;
  isAcceptedSelected: boolean;
  isAcceptedUndefinedSelected: boolean;
  isInProgressSelected: boolean;
  vulnerabilities: IVulnDataTypeAttr[];
}

export type { IExternalBtsFieldProps };
