import type { IVulnDataType } from "../../types";

interface IExternalBtsFieldProps {
  isAcceptedSelected: boolean;
  isAcceptedUndefinedSelected: boolean;
  isInProgressSelected: boolean;
  vulnerabilities: IVulnDataType[];
}

export { IExternalBtsFieldProps };
