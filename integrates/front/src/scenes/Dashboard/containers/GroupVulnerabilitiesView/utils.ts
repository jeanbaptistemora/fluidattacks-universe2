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

export { filterByState, filterByTreatment };
