/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IHeaderQueryResult {
  finding: {
    closedVulns: number;
    currentState: string;
    hacker?: string;
    id: string;
    minTimeToRemediate: number;
    openVulns: number;
    releaseDate: string | null;
    severityScore: number;
    state: "closed" | "default" | "open";
    title: string;
  };
}

interface IRemoveFindingResultAttr {
  removeFinding?: {
    success: boolean;
  };
}

export type { IHeaderQueryResult, IRemoveFindingResultAttr };
