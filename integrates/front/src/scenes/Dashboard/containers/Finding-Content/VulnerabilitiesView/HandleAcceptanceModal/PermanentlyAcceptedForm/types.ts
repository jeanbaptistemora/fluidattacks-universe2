import type { IVulnerabilitiesAttr } from "../../types";

interface IPermanentlyAcceptedFormProps {
  onCancel: () => void;
  refetchData: () => void;
  vulnerabilities: IVulnerabilitiesAttr[];
}

interface IFormValues {
  justification: string;
}

export type { IFormValues, IPermanentlyAcceptedFormProps };
