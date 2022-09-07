/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { IVulnDataAttr } from "../types";

interface IAcceptedUndefinedTableProps {
  acceptanceVulns: IVulnDataAttr[];
  isAcceptedUndefinedSelected: boolean;
  setAcceptanceVulns: (vulns: IVulnDataAttr[]) => void;
}

export type { IAcceptedUndefinedTableProps };
