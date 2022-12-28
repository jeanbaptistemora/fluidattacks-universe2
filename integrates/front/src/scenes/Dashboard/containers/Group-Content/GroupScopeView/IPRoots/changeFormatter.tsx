import React from "react";

import { Switch } from "components/Switch";

export const changeFormatter = (
  row: Record<string, string>,
  changeFunction: (arg1: Record<string, string>) => void
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
