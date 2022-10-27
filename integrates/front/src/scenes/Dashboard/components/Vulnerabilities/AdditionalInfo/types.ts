/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IVulnInfoAttr {
  closingDate: string | null;
  commitHash: string | null;
  cycles: string;
  efficacy: string;
  hacker?: string;
  lastReattackRequester: string;
  lastRequestedReattackDate: string | null;
  lastStateDate: string;
  lastTreatmentDate: string;
  reportDate: string;
  severity: string | null;
  source: string;
  stream: string | null;
  treatment: string;
  treatmentAcceptanceDate: string | null;
  treatmentAssigned: string | null;
  treatmentChanges: string;
  treatmentJustification: string | null;
  vulnerabilityType: string;
}

interface IGetVulnAdditionalInfoAttr {
  vulnerability: IVulnInfoAttr;
}

export type { IGetVulnAdditionalInfoAttr, IVulnInfoAttr };
