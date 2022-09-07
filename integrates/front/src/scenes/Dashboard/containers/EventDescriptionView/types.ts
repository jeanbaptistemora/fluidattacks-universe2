/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IAffectedReattacks {
  findingId: string;
  where: string;
  specific: string;
}

interface IEventDescriptionData {
  event: {
    affectedReattacks: IAffectedReattacks[];
    closingDate: string;
    hacker: string;
    client: string;
    detail: string;
    eventType: string;
    eventStatus: string;
    id: string;
    otherSolvingReason: string | null;
    solvingReason: string | null;
  };
}

interface IDescriptionFormValues {
  eventType: string;
  otherSolvingReason: string | null;
  solvingReason: string | null;
}

interface IRejectEventSolutionResultAttr {
  rejectEventSolution: {
    success: boolean;
  };
}

interface IUpdateEventAttr {
  updateEvent: {
    success: boolean;
  };
}

interface IUpdateEventSolvingReasonAttr {
  updateEventSolvingReason: {
    success: boolean;
  };
}

export type {
  IAffectedReattacks,
  IEventDescriptionData,
  IDescriptionFormValues,
  IRejectEventSolutionResultAttr,
  IUpdateEventAttr,
  IUpdateEventSolvingReasonAttr,
};
