/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IGroupData {
  group: {
    deletionDate: string;
    organization: string;
    serviceAttributes: string[];
  };
}

interface IGroupRoute {
  setUserRole: (userRole: string | undefined) => void;
}

export type { IGroupData, IGroupRoute };
