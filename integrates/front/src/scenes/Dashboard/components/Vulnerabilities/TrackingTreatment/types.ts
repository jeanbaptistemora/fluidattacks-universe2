/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

interface IVulnTreatmentAttr {
  historicTreatment: IHistoricTreatment[];
}

interface IGetVulnTreatmentAttr {
  vulnerability: IVulnTreatmentAttr;
}

export type { IGetVulnTreatmentAttr };
