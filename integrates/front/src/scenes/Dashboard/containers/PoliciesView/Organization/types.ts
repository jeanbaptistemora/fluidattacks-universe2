/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { IVulnerabilityPoliciesData } from "scenes/Dashboard/containers/PoliciesView/Organization/VulnerabilityPolicies/types";
import type { IPoliciesData } from "scenes/Dashboard/containers/PoliciesView/types";

interface IOrganizationPolicies {
  organizationId: string;
}

interface IOrganizationPoliciesData {
  organization: IPoliciesData & {
    findingPolicies: IVulnerabilityPoliciesData[];
    name: string;
  };
}

export type { IOrganizationPolicies, IOrganizationPoliciesData };
