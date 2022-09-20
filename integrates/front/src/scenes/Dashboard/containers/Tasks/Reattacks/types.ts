/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface ITodoFindingToReattackAttr {
  age: number;
  currentState: string;
  groupName: string;
  hacker: string;
  id: string;
  lastVulnerability: number;
  openVulnerabilities: number;
  severityScore: number;
  state: string;
  title: string;
}

interface IVulnerabilityAttr {
  id: string;
  groupName: string;
  lastRequestedReattackDate: string;
  finding: ITodoFindingToReattackAttr;
}

interface IGetTodoReattacks {
  me: {
    reattacks: {
      edges: { node: IVulnerabilityAttr }[];
    };
  };
}
interface IVulnFormatted extends IVulnerabilityAttr {
  oldestReattackRequestedDate: string;
}

export type {
  IGetTodoReattacks,
  IVulnFormatted,
  ITodoFindingToReattackAttr,
  IVulnerabilityAttr,
};
