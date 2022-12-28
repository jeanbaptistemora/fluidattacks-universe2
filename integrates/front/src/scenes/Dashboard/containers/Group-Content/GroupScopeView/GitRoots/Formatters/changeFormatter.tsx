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
