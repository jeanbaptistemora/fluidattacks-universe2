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
      checked={!("state" in row) || row.state !== "SAFE"}
      label={{ off: "Safe", on: "Vulnerable" }}
      onChange={handleOnChange}
    />
  );
};
