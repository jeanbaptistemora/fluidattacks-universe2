/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { IVulnerability } from "./types";

const filterByState = (
  state: string
): ((vulnerability: IVulnerability) => boolean) => {
  return (vulnerability: IVulnerability): boolean => {
    return vulnerability.currentState === state;
  };
};

const filterByTreatment = (
  treatment: string
): ((vulnerability: IVulnerability) => boolean) => {
  return (vulnerability: IVulnerability): boolean => {
    return vulnerability.treatment === treatment;
  };
};

const formatVulnAttribute: (state: string) => string = (
  state: string
): string => {
  const vulnParameters: Record<string, string> = {
    currentState: "stateStatus",
    treatment: "treatment",
    verification: "verificationStatus",
  };

  return vulnParameters[state];
};

const unformatTreatment: (field: string) => string = (
  field: string
): string => {
  const translationParameters: Record<string, string> = {
    "In progress": "IN_PROGRESS",
    New: "NEW",
    "Permanently accepted": "ACCEPTED_UNDEFINED",
    Rejected: "REJECTED",
    "Temporarily accepted": "ACCEPTED",
  };

  return translationParameters[field.replace(" (Pending approval)", "")];
};

export {
  filterByState,
  filterByTreatment,
  formatVulnAttribute,
  unformatTreatment,
};
