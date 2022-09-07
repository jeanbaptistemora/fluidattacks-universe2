/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

interface IAcceptanceDateFieldProps {
  isAcceptedSelected: boolean;
  lastTreatment: IHistoricTreatment;
}

export type { IAcceptanceDateFieldProps };
