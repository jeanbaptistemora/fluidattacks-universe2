/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { IVulnRowAttr } from "../types";

interface IAdditionalInfoProps {
  canRetrieveHacker: boolean;
  canSeeSource: boolean;
  vulnerability: IVulnRowAttr;
}

interface IFormValues {
  source: string;
}

interface IGetVulnAdditionalInfoAttr {
  vulnerability: IVulnInfoAttr;
}

interface IUpdateVulnerabilityDescriptionAttr {
  updateVulnerabilityDescription: {
    success: boolean;
  };
}

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

export type {
  IAdditionalInfoProps,
  IFormValues,
  IGetVulnAdditionalInfoAttr,
  IUpdateVulnerabilityDescriptionAttr,
  IVulnInfoAttr,
};
