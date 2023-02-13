import type { IVulnerabilitiesAttr } from "../../types";

interface ISubmittedFormProps {
  groupName: string;
  findingId?: string;
  onCancel: () => void;
  refetchData: () => void;
  vulnerabilities: IVulnerabilitiesAttr[];
}

interface IFormValues {
  rejectionReasons: string[];
  otherRejectionReason?: string;
}

export type { IFormValues, ISubmittedFormProps };
