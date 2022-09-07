/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { IPoliciesData } from "scenes/Dashboard/containers/PoliciesView/types";

interface IGroupPoliciesData {
  group: IPoliciesData & {
    name: string;
  };
}

export type { IGroupPoliciesData };
