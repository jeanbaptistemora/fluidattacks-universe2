/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IComplianceAttr {
  id: string;
  name: string;
  compliance: {
    nonComplianceLevel: number | null;
  };
}

interface IOrganizationComplianceOverviewProps {
  organizationId: string;
}

export type { IComplianceAttr, IOrganizationComplianceOverviewProps };
