/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface ITodoFindingToReattackAttr {
  groupName: string;
  id: string;
  title: string;
  vulnerabilitiesToReattackConnection: IVulnerabilitiesConnection;
  verificationSummary: {
    requested: string;
  };
}

interface IGetTodoReattacks {
  me: {
    findingReattacks: ITodoFindingToReattackAttr[];
  };
}

interface IVulnerabilityAttr {
  id: string;
  lastRequestedReattackDate: string;
}

interface IVulnerabilityEdge {
  node: IVulnerabilityAttr;
}

interface IVulnerabilitiesConnection {
  edges: IVulnerabilityEdge[];
}
interface IFindingFormatted extends ITodoFindingToReattackAttr {
  oldestReattackRequestedDate: string;
  url: string;
}

export type {
  IFindingFormatted,
  IGetTodoReattacks,
  ITodoFindingToReattackAttr,
  IVulnerabilityAttr,
  IVulnerabilityEdge,
};
