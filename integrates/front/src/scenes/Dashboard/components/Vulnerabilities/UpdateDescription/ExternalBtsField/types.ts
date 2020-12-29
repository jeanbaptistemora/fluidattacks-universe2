import type { IVulnDataTypeAttr } from "../../types";

interface IExternalBtsFieldProps {
  isAcceptedSelected: boolean;
  isAcceptedUndefinedSelected: boolean;
  isInProgressSelected: boolean;
  vulnerabilities: IVulnDataTypeAttr[];
}

export { IExternalBtsFieldProps };
