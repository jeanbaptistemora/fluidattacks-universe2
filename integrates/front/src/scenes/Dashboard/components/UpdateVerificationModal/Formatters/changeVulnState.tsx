/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { Switch } from "components/Switch";

export const changeVulnStateFormatter = (
  row: Readonly<Record<string, string>>,
  changeFunction: (arg1: Record<string, string>) => void
): JSX.Element => {
  function handleOnChange(): void {
    changeFunction(row);
  }

  return (
    <Switch
      checked={!("currentState" in row) || row.currentState !== "closed"}
      label={{ off: "closed", on: "open" }}
      onChange={handleOnChange}
    />
  );
};
