/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ExecutionResult } from "graphql";

interface IReattackVuln {
  affected?: boolean;
  findingId: string;
  id: string;
  specific: string;
  where: string;
}

interface IFinding {
  id: string;
  title: string;
  verified: boolean;
}

interface IFindingsQuery {
  group: {
    name: string;
    findings: IFinding[];
  };
}

interface IAffectedReattackModal {
  findings: IReattackVuln[];
  clearSelected: () => void;
  handleCloseModal: () => void;
  setRequestState: () => void;
}

interface IAffectedAccordionProps {
  findings: IFinding[];
}

interface IRequestVulnerabilitiesHold {
  requestVulnerabilitiesHold: {
    success: boolean;
  };
}

type RequestVulnerabilitiesHoldResult =
  ExecutionResult<IRequestVulnerabilitiesHold>;

export type {
  IAffectedAccordionProps,
  IReattackVuln,
  IFinding,
  IFindingsQuery,
  IAffectedReattackModal,
  RequestVulnerabilitiesHoldResult,
};
