import type { IVulnerabilitiesAttr } from "../../types";

interface IZeroRiskFormProps {
  groupName: string;
  findingId?: string;
  onCancel: () => void;
  refetchData: () => void;
  vulnerabilities: IVulnerabilitiesAttr[];
}

interface IFormValues {
  justification: string;
}

export type { IFormValues, IZeroRiskFormProps };
