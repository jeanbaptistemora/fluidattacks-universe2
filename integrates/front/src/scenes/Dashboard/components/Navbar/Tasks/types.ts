/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IGetMeVulnerabilitiesAssignedIds {
  me: {
    vulnerabilitiesAssigned: { id: string }[];
    userEmail: string;
  };
}

export type { IGetMeVulnerabilitiesAssignedIds };
