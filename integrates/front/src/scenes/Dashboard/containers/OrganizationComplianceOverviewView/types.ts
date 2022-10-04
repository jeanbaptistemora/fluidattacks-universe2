/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IStandardComplianceAttr {
  avgOrganizationComplianceLevel: number;
  bestOrganizationComplianceLevel: number;
  complianceLevel: number;
  standardTitle: string;
  worstOrganizationComplianceLevel: number;
}

interface IOrganizationAttr {
  id: string;
  name: string;
  compliance: {
    complianceLevel: number | null;
    complianceWeeklyTrend: number | null;
    estimatedDaysToFullCompliance: number | null;
    standards: IStandardComplianceAttr[];
  };
}

interface IOrganizationComplianceOverviewProps {
  organizationId: string;
}

export type {
  IOrganizationAttr,
  IOrganizationComplianceOverviewProps,
  IStandardComplianceAttr,
};
