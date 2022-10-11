/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IGroupAttr {
  name: string;
}

interface IOrganizationComplianceStandardsProps {
  organizationId: string;
}

interface IUnfulfilledRequirementAttr {
  id: string;
  title: string;
}

interface IUnfulfilledStandardAttr {
  title: string;
  unfulfilledRequirements: IUnfulfilledRequirementAttr[];
}

export type {
  IGroupAttr,
  IOrganizationComplianceStandardsProps,
  IUnfulfilledStandardAttr,
  IUnfulfilledRequirementAttr,
};
