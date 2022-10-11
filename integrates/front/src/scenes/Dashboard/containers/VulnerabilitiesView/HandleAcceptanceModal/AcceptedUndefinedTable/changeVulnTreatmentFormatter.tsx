/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import type { IVulnDataAttr } from "../types";
import { Switch } from "components/Switch";

export const changeVulnTreatmentFormatter = (
  row: IVulnDataAttr,
  changeFunction: (arg1: IVulnDataAttr) => void
): JSX.Element => {
  function handleOnChange(): void {
    changeFunction(row);
  }

  return (
    <Switch
      checked={row.acceptance !== "REJECTED"}
      label={{ off: "REJECTED", on: "APPROVED" }}
      onChange={handleOnChange}
    />
  );
};
