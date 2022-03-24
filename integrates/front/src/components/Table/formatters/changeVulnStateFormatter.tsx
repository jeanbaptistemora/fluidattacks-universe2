import React from "react";

import { Switch } from "components/Switch";
import type { IHeaderConfig } from "components/Table/types";

export const changeVulnStateFormatter = (
  _value: string,
  row: Readonly<Record<string, string>>,
  _rowIndex: number,
  key: Readonly<IHeaderConfig>
): JSX.Element => {
  function handleOnChange(): void {
    if (key.changeFunction !== undefined) {
      key.changeFunction(row);
    }
  }

  return (
    <Switch
      checked={!("currentState" in row) || row.currentState !== "closed"}
      label={{ off: "closed", on: "open" }}
      onChange={handleOnChange}
    />
  );
};
