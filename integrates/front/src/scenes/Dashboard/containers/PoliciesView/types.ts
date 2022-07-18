interface IPoliciesData {
  maxAcceptanceDays: string;
  maxAcceptanceSeverity: string;
  maxNumberAcceptances: string;
  minAcceptanceSeverity: string;
  minBreakingSeverity: string;
  vulnerabilityGracePeriod: string;
}

interface IPolicies extends IPoliciesData {
  handleSubmit: (values: IPoliciesData) => void;
  loadingPolicies: boolean;
  permission: string;
  savingPolicies: boolean;
}

export type { IPoliciesData, IPolicies };
