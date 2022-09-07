/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
  tooltipMessage?: string;
}

export type { IPoliciesData, IPolicies };
