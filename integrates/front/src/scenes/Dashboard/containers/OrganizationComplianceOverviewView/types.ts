/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IStandardComplianceAttr {
  avgOrganizationNonComplianceLevel: number;
  bestOrganizationNonComplianceLevel: number;
  nonComplianceLevel: number;
  standardTitle: string;
  worstOrganizationNonComplianceLevel: number;
}

interface IOrganizationAttr {
  id: string;
  name: string;
  compliance: {
    nonComplianceLevel: number | null;
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
