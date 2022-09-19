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
  lastRequestedReattackDate: string;
  finding: ITodoFindingToReattackAttr;
}

interface IVulnerabilityEdges {
  node: IVulnerabilityAttr[];
}
interface ITodoGroupAttr {
  vulnerabilities: {
    edges: IVulnerabilityEdges[];
  };
}
interface ITodoOrganizationAttr {
  groups: ITodoGroupAttr[];
  name: string;
}

interface IGetTodoReattacks {
  me: {
    organizations: ITodoOrganizationAttr[];
  };
}

interface IVulnFormatted extends IVulnerabilityAttr {
  oldestReattackRequestedDate: string;
}

export type {
  IGetTodoReattacks,
  IVulnFormatted,
  ITodoFindingToReattackAttr,
  ITodoGroupAttr,
  ITodoOrganizationAttr,
  IVulnerabilityAttr,
  IVulnerabilityEdges,
};
