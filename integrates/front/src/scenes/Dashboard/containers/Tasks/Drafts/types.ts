/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface ITodoDraftAttr {
  currentState: string;
  groupName: string;
  hacker: string;
  id: string;
  openVulnerabilities: number;
  reportDate: string | null;
  severityScore: number;
  title: string;
}

interface ITodoGroupAttr {
  drafts: ITodoDraftAttr[];
}

interface ITodoOrganizationAttr {
  groups: ITodoGroupAttr[];
  name: string;
}

interface IGetTodoDrafts {
  me: {
    organizations: ITodoOrganizationAttr[];
  };
}

export type {
  IGetTodoDrafts,
  ITodoDraftAttr,
  ITodoGroupAttr,
  ITodoOrganizationAttr,
};
