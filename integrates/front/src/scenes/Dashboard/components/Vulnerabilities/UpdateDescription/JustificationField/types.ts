/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

interface IJustificationFieldProps {
  isTreatmentPristine: boolean;
  lastTreatment: IHistoricTreatment;
}

export type { IJustificationFieldProps };
