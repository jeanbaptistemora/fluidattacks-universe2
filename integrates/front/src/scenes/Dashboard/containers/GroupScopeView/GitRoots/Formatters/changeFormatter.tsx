/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import type { IGitRootData } from "../../types";
import { Switch } from "components/Switch";

export const changeFormatter = (
  row: IGitRootData,
  changeFunction: (arg: IGitRootData) => void
): JSX.Element => {
  function handleOnChange(): void {
    changeFunction(row);
  }

  return (
    <Switch
      checked={!("state" in row) || row.state.toUpperCase() !== "INACTIVE"}
      label={{ off: "Inactive", on: "Active" }}
      onChange={handleOnChange}
    />
  );
};
